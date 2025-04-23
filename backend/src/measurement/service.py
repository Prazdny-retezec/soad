import logging
import time
from datetime import datetime, timedelta
from typing import List

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from common.enum import ImageFormat
from controller.acoustic_emission import AcousticEmissionController
from controller.mock.acoustic_emission import AcousticEmissionMockController
from controller.mock.multi_spectral_camera import MultiSpectralCameraMockController
from controller.mock.rgb_camera import RgbCameraMockController
from controller.multi_spectral_camera import MultiSpectralCameraController
from controller.rgb_camera import RgbCameraController
from database import get_db, sessionLocal
from scheduler import get_scheduler
from measurement.dto import MeasurementCreateDto, MeasurementUpdateDto, MeasurementCreatePeriodicDto
from measurement.model import Measurement, MeasurementState, MeasurementResult
from settings import Settings


class MeasurementService:
    def __init__(self, db: Session = Depends(get_db), scheduler: AsyncIOScheduler = Depends(get_scheduler)):
        self.db = db
        self.scheduler = scheduler

    def get_measurement(self, measurement_id: int) -> Measurement:
        query = self.db.query(Measurement).filter(
            (Measurement.id == measurement_id) &
            (Measurement.deleted_at.is_(None))
        )
        entity = query.first()

        if entity is None:
            raise HTTPException(status_code=404, detail="Measurement not found")
        else:
            return entity

    def list_measurements(self) -> List[Measurement]:
        query = (self.db
                 .query(Measurement)
                 .filter(Measurement.deleted_at.is_(None))
                 .order_by(Measurement.planned_at.asc())
        )

        measurements = query.all()
        return measurements

    def create_measurement(self, dto: MeasurementCreateDto) -> Measurement:
        # map DTO to entity
        measurement = Measurement(
            name=dto.name,
            description=dto.description,
            planned_at=dto.plan_at,
            ae_delta=dto.ae_delta,
            state=MeasurementState.NEW,
        )

        # TODO validation

        # create
        measurement = self.__save_measurement(measurement)

        # plan
        if dto.plan_at is not None:
            measurement = self.plan_measurement(measurement.id, None, None)

        return measurement

    def create_periodic_measurement(self, dto: MeasurementCreatePeriodicDto) -> List[Measurement]:
        measurements = []

        # TODO validation

        current_time = dto.plan_from
        while current_time <= dto.plan_to:
            single_dto = MeasurementCreateDto(name=dto.name, description=dto.description,
                                              plan_at=current_time, ae_delta=dto.ae_delta)
            measurements.append(self.create_measurement(single_dto))
            current_time += dto.period

        return measurements

    def update_measurement(self, measurement_id: int, dto: MeasurementUpdateDto) -> Measurement:
        measurement = self.get_measurement(measurement_id)

        # map DTO to entity
        measurement.name = dto.name
        measurement.description = dto.description

        # TODO validation

        # update entity in database
        measurement = self.__save_measurement(measurement)
        return measurement

    def delete_measurement(self, measurement_id: int):
        query = (self.db
            .query(Measurement)
            .filter(
                (Measurement.id == measurement_id) &
                (Measurement.deleted_at.is_(None))
            )
        )

        measurement: Measurement | None = query.first()

        # ignore deleted measurement
        if measurement is None:
            return

        # remove run of planned job
        if measurement.scheduler_job_id is not None:
            self.scheduler.remove_job(measurement.scheduler_job_id)
            measurement.scheduler_job_id = None

        # soft delete
        measurement.deleted_at = datetime.now()
        self.db.add(measurement)
        self.db.commit()

    def plan_measurement(
            self,
            measurement_id: int,
            plan_at: datetime | None,
            ae_delta: timedelta | None
    ) -> Measurement:
        measurement = self.get_measurement(measurement_id)

        # override planning attributes if they are sent
        if plan_at is not None:
            measurement.planned_at = plan_at
        if ae_delta is not None:
            measurement.ae_delta = ae_delta

        # TODO validations overriding measurements by time, measurement in bad state, don't plan at history date ...

        try:
            # plan measurements via scheduler
            job = self.scheduler.add_job(
                func=MeasurementService.proceed_measuring,
                args=[measurement.id],
                trigger="date",

                # we shift the start so we can collect AE before capturing images
                run_date=measurement.planned_at - measurement.ae_delta
            )

            # change state to planned
            measurement.state = MeasurementState.PLANNED
            measurement.scheduler_job_id = job.id

            # save updated measurement
            measurement = self.__save_measurement(measurement)

            logging.debug(f"Planned execution of measurement at {plan_at}")
        except Exception as e:
            logging.error(e)
            measurement.state = MeasurementState.ERROR
            measurement = self.__save_measurement(measurement)

        return measurement

    def unplan_measurement(self, measurement_id: int) -> Measurement:
        measurement = self.get_measurement(measurement_id)

        # TODO validations: bad state, already running, ....

        # change state back to new
        measurement.state = MeasurementState.NEW

        # remove scheduled job from scheduler
        self.scheduler.remove_job(measurement.scheduler_job_id)

        # save measurement
        measurement = self.__save_measurement(measurement)
        return measurement

    @staticmethod  # must be static due to serialization of job
    async def proceed_measuring(measurement_id: int):
        # must have explicitly declared session due to serialization of job
        db = sessionLocal()

        def change_state(mes: Measurement, state: MeasurementState) -> Measurement:
            mes.state = state
            db.add(mes)
            db.commit()
            db.refresh(mes)

            return mes

        logging.debug(f"Starting measurement for {measurement_id}")
        measurement = db.query(Measurement).filter(Measurement.id == measurement_id).first()

        if measurement is None or measurement.state != MeasurementState.PLANNED:
            logging.warn(f"Missing measurement with id: {measurement_id}")
            return

        logging.debug(f"Downloading for measurement {measurement_id}")
        measurement.started_at = datetime.now()
        measurement = change_state(measurement, MeasurementState.DOWNLOADING)

        # choose controllers
        controllers = MeasurementService.__choose_controllers()
        rgb_camera_class = controllers["rgb"]
        ms_camera_class = controllers["ms"]
        ae_class = controllers["ae"]

        # TODO replace time.sleep by multi-threading implementation, start measuring async and after that join threads
        # and collect all results
        try:
            # TODO turn on acoustic emission
            time.sleep(measurement.ae_delta.seconds)

            # TODO start capturing via multi-spectral camera

            # RGB camera capture
            with rgb_camera_class(1920, 1080) as rgb_camera:
                rgb_camera.capture_image("/home/petr/Git/soad/backend/test_data", 90, ImageFormat.PNG) # TODO change path

            time.sleep(measurement.ae_delta.seconds)
            # TODO stop acoustic emission
            # TODO stop multi-spectral camera
            # TODO collect data from acoustic emission
            # TODO collect data from multi-spectral camera

            logging.debug(f"Zipping measurement {measurement_id}")
            time.sleep(3)
            measurement = change_state(measurement, MeasurementState.ZIPPING)
            # TODO zip data together

            logging.debug(f"Uploading measurement {measurement_id}")
            time.sleep(3)
            measurement = change_state(measurement, MeasurementState.UPLOADING)
            # TODO upload data to cloud

            # TODO use actual result and actual cloud URL
            logging.debug(f"Finishing measurement {measurement_id}")
            measurement.result = MeasurementResult(
                cloud_url="https://www.icegif.com/wp-content/uploads/2023/01/icegif-162.gif",
                measurement_id=measurement_id
            )
            measurement.finished_at = datetime.now()
            measurement = change_state(measurement, MeasurementState.FINISHED)
        except Exception as e:
            logging.error(e)
            measurement.result = MeasurementResult(error=str(e), measurement_id=measurement_id)
            change_state(measurement, MeasurementState.ERROR)
        finally:
            db.close()

    @staticmethod
    def __choose_controllers():
        if Settings().mock_controller:
            return {
                "rgb": RgbCameraMockController,
                "ms": MultiSpectralCameraMockController,
                "ae": AcousticEmissionMockController
            }
        else:
            return {
                "rgb": RgbCameraController,
                "ms": MultiSpectralCameraController,
                "ae": AcousticEmissionController
            }

    def __save_measurement(self, measurement: Measurement) -> Measurement:
        self.db.add(measurement)
        self.db.commit()
        self.db.refresh(measurement)

        return measurement
