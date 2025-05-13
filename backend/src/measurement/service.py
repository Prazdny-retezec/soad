import glob
import logging
import os
import threading
import time
import uuid
from datetime import datetime, timedelta
from typing import List

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from common.enum import ImageFormat
from controllers import get_acoustic_emission_controller, get_rgb_camera_controller, get_ms_camera_controller
from database import get_db, sessionLocal
from measurement.dto import MeasurementCreateDto, MeasurementUpdateDto, MeasurementCreatePeriodicDto
from measurement.model import Measurement, MeasurementState, MeasurementResult
from scheduler import get_scheduler
from sensor.model import SensorSettings

from google_drive.gdrive_handler import gdrive_auth, upload_zip_file
from settings import AppSettings
from zipper import create_zip_archive


class MeasurementService:
    def __init__(self, db: Session = Depends(get_db), scheduler: AsyncIOScheduler = Depends(get_scheduler)):
        self.db = db
        self.scheduler = scheduler
        
    def check_for_conflicting_measurements(self, plan_from: datetime) -> bool:
        # Kontrola, zda již existuje měření s daným časem
        conflict = self.db.query(Measurement).filter(
            (Measurement.deleted_at.is_(None)) &
            (Measurement.planned_at == plan_from)  # Kontrola, zda se čas naplánovaného měření shoduje
        ).first()
        return conflict is not None

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
            duration=dto.duration,
            state=MeasurementState.NEW,
        )
        measurement.sensor_settings = dto.sensor_settings.to_entity()

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
            single_dto = MeasurementCreateDto(name=dto.name, description=dto.description, plan_at=current_time,
                                              ae_delta=dto.ae_delta, duration=dto.duration, sensor_settings=dto.sensor_settings)
            measurements.append(self.create_measurement(single_dto))
            current_time += dto.duration

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

            logging.info(f"Planned execution of measurement at {plan_at}")
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
        measurement.planned_at = None

        # remove scheduled job from scheduler
        if measurement.scheduler_job_id is not None:
            self.scheduler.remove_job(measurement.scheduler_job_id)

        # save measurement
        measurement = self.__save_measurement(measurement)
        return measurement

    @staticmethod  # must be static due to serialization of job
    async def proceed_measuring(measurement_id: int):
        # must have explicitly declared session due to serialization of job
        db = sessionLocal()
        app_settings = AppSettings()

        def change_state(mes: Measurement, state: MeasurementState) -> Measurement:
            mes.state = state
            db.add(mes)
            db.commit()
            db.refresh(mes)

            return mes

        logging.info(f"Starting measurement for {measurement_id}")
        measurement = db.query(Measurement).filter(Measurement.id == measurement_id).first()

        if measurement is None or measurement.state != MeasurementState.PLANNED:
            logging.warn(f"Missing measurement with id: {measurement_id}")
            return

        logging.info(f"Downloading for measurement {measurement_id}")
        measurement.started_at = datetime.now()
        measurement = change_state(measurement, MeasurementState.DOWNLOADING)

        try:
            # setup thread for each sensor
            ae_thread = threading.Thread(
                target=MeasurementService.acoustic_emission_measuring,
                args=(measurement.ae_delta, measurement.duration)
            )
            rgb_thread = threading.Thread(
                target=MeasurementService.rgb_camera_measuring,
                args=(measurement.sensor_settings,)
            )
            ms_thread = threading.Thread(
                target=MeasurementService.ms_camera_measuring,
                args=(measurement.sensor_settings,)
            )

            # start acoustic emission
            ae_thread.start()

            # wait till AE data are collected for ae_delta time
            time.sleep(measurement.ae_delta.seconds)

            # start other sensors
            ms_thread.start()
            rgb_thread.start()

            # wait till all sensors are done
            ae_thread.join()
            rgb_thread.join()
            ms_thread.join()

            # zip produced data files
            logging.info(f"Zipping measurement {measurement_id}")
            measurement = change_state(measurement, MeasurementState.ZIPPING)

            files_to_zip = glob.glob(app_settings.output_dir + "/*")
            zip_file_name = os.path.join(app_settings.output_dir, f"{measurement_id}.zip")
            create_zip_archive(files_to_zip, zip_file_name)

            # upload zipped files to google drive
            logging.info(f"Uploading measurement {measurement_id}")
            measurement = change_state(measurement, MeasurementState.UPLOADING)

            gdrive_service = gdrive_auth()
            gdrive_url = upload_zip_file(
                gdrive_service=gdrive_service,
                path_to_local_zip_file=zip_file_name,
                gdrive_file_name=measurement.name
            )

            logging.info(f"Finishing measurement {measurement_id}")
            measurement.result = MeasurementResult(
                cloud_url=gdrive_url,
                measurement_id=measurement_id
            )
            measurement.finished_at = datetime.now()
            measurement = change_state(measurement, MeasurementState.FINISHED)

            # delete uploaded files
            files_to_delete = glob.glob(app_settings.output_dir + "/*")
            for file in files_to_delete:
                os.remove(file)
                logging.info(f"Deleted file: {file}")

        except Exception as e:
            logging.error(e)
            measurement.result = MeasurementResult(error=str(e), measurement_id=measurement_id)
            change_state(measurement, MeasurementState.ERROR)
        finally:
            db.close()

    @staticmethod
    def acoustic_emission_measuring(ae_delta: timedelta, duration: timedelta):
        with get_acoustic_emission_controller() as acoustic_emission:
            # TODO emission.configure() -> SensorSettings
            acoustic_emission.start_recording(str(uuid.uuid4()), 0)
            # beginning of acoustic emission collection (before cameras)
            time.sleep(ae_delta.seconds)

            # measuring itself
            time.sleep(duration.seconds)

            # end of acoustic emission measuring (after cameras)
            time.sleep(ae_delta.seconds)

            # saving measured data to csv file
            acoustic_emission.stop_recording()

    @staticmethod
    def rgb_camera_measuring(sensors: SensorSettings):
        with get_rgb_camera_controller(width=sensors.rgb_image_width, height=sensors.rgb_image_height) as rgb_camera:
            for i in range(0, sensors.rgb_image_count):
                rgb_camera.capture_image(quality=sensors.rgb_image_quality, img_format=sensors.rgb_image_format)
                time.sleep(sensors.rgb_sampling_delay)

    @staticmethod
    def ms_camera_measuring(sensors: SensorSettings):
        ms_camera = get_ms_camera_controller()

        for i in range(0, sensors.ms_image_count):
            ms_camera.start_capturing(
                img_format=ImageFormat.PNG,
                width=sensors.ms_image_width,
                height=sensors.ms_image_height,
                interval=sensors.ms_sampling_delay,
                exposure_time=sensors.ms_exposure_time
            )

            ms_camera.stop_capturing()
            time.sleep(sensors.ms_sampling_delay)

    def __save_measurement(self, measurement: Measurement) -> Measurement:
        self.db.add(measurement)
        self.db.commit()
        self.db.refresh(measurement)

        return measurement

    def _is_time_taken(self, plan_at: datetime) -> bool:
        # Check if any existing measurement overlaps with the given time
        overlapping_measurement = self.db.query(Measurement).filter(
            Measurement.deleted_at.is_(None),
            Measurement.planned_at == plan_at
        ).first()

        return overlapping_measurement is not None
