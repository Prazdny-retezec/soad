import logging
import time
from datetime import datetime, timedelta
from typing import List
import re
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from common.enum import ImageFormat
from controller.rgb_camera import RgbCameraController
from database import get_db, sessionLocal
from scheduler import get_scheduler
from measurement.dto import MeasurementCreateDto, MeasurementUpdateDto, MeasurementCreatePeriodicDto
from measurement.model import Measurement, MeasurementState, MeasurementResult


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
    """
    def create_measurement(self, dto: MeasurementCreateDto) -> Measurement:
        logging.debug(f"Creating measurement with data: {dto}")
        try:
            # Map DTO to entity
            measurement = Measurement(
                name=dto.name,
                description=dto.description,
                planned_at=dto.plan_at,
                ae_delta=dto.ae_delta,
                state=MeasurementState.NEW,
            )
            measurement = self.__save_measurement(measurement)
            return measurement
        except Exception as e:
            logging.error(f"Error while creating measurement: {e}")
            raise HTTPException(status_code=500, detail="Error creating measurement")

    def create_periodic_measurement(self, dto: MeasurementCreatePeriodicDto) -> List[Measurement]:
        # List to store created measurements
        measurements = []
        
        # Loop through the given period and create measurements
        current_time = dto.plan_from
        while current_time < dto.plan_to:
            # Create measurement for each period
            measurement = Measurement(
                name=dto.name,
                description=dto.description,
                planned_at=current_time,
                ae_delta=dto.ae_delta,
                state=MeasurementState.NEW,
            )

            # Save the measurement to the database
            measurement = self.__save_measurement(measurement)
            measurements.append(measurement)

            # Increment the current_time by the period
            current_time += dto.period

        return measurements
"""
    def create_measurement(self, dto: MeasurementCreateDto) -> Measurement:
        logging.debug(f"Creating measurement with data: {dto}")
        try:
            # Check if plan_at is provided, and set the state accordingly
            state = MeasurementState.PLANNED if dto.plan_at else MeasurementState.NEW

            # Map DTO to entity
            measurement = Measurement(
                name=dto.name,
                description=dto.description,
                planned_at=dto.plan_at,
                ae_delta=dto.ae_delta,
                state=state,
            )
            measurement = self.__save_measurement(measurement)
            return measurement
        except Exception as e:
            logging.error(f"Error while creating measurement: {e}")
            raise HTTPException(status_code=500, detail="Error creating measurement")
    def create_periodic_measurement(self, dto: MeasurementCreatePeriodicDto) -> List[Measurement]:
        # List to store created measurements
        measurements = []
        
        # Loop through the given period and create measurements
        current_time = dto.plan_from
        while current_time < dto.plan_to:
            # Set state to PLANNED for all periodic measurements
            state = MeasurementState.PLANNED

            # Create measurement for each period
            measurement = Measurement(
                name=dto.name,
                description=dto.description,
                planned_at=current_time,
                ae_delta=dto.ae_delta,
                state=state,
            )

            # Save the measurement to the database
            measurement = self.__save_measurement(measurement)
            measurements.append(measurement)

            # Increment the current_time by the period
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
        try:
            # Query the measurement by ID and check if it exists
            query = (self.db
                .query(Measurement)
                .filter(
                    (Measurement.id == measurement_id) &
                    (Measurement.deleted_at.is_(None))
                )
            )

            measurement = query.first()

            if measurement is None:
                raise HTTPException(status_code=404, detail="Measurement not found")

            # Perform any related job removal and soft delete
            if measurement.scheduler_job_id:
                try:
                    self.scheduler.remove_job(measurement.scheduler_job_id)
                except Exception as e:
                    logging.error(f"Error removing job {measurement.scheduler_job_id}: {e}")
                measurement.scheduler_job_id = None

            measurement.deleted_at = datetime.now()
            self.db.add(measurement)
            self.db.commit()

            return measurement
        except Exception as e:
            logging.error(f"Error deleting measurement with ID {measurement_id}: {e}")
            self.db.rollback()
            raise HTTPException(status_code=500, detail="Error deleting measurement")


    def plan_measurement(self, measurement_id: int, plan_at: datetime, ae_delta: timedelta) -> Measurement:
        measurement = self.get_measurement(measurement_id)

        # Update the measurement attributes
        measurement.planned_at = plan_at
        measurement.ae_delta = ae_delta

        # Plan the measurement via scheduler
        try:
            job = self.scheduler.add_job(
                func=self.proceed_measuring,
                args=[measurement.id],
                trigger="date",
                run_date=plan_at - ae_delta
            )

            # Update state to PLANNED and assign job ID
            measurement.state = MeasurementState.PLANNED
            measurement.scheduler_job_id = job.id

            measurement = self.__save_measurement(measurement)
            return measurement

        except Exception as e:
            measurement.state = MeasurementState.ERROR
            measurement = self.__save_measurement(measurement)
            raise HTTPException(status_code=500, detail=f"Error planning measurement: {str(e)}")

    def unplan_measurement(self, measurement_id: int) -> Measurement:
        measurement = self.get_measurement(measurement_id)

        # Change state back to new
        measurement.state = MeasurementState.NEW
        measurement.planned_at = None  # Remove the planned_at value

        # Save updated measurement
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

        # TODO replace time.sleep by multi-threading implementation, start measuring async and after that join threads
        # and collect all results
        try:
            # TODO turn on acoustic emission
            time.sleep(measurement.ae_delta.seconds)

            # TODO start capturing via multi-spectral camera

            # RGB camera capture
            with RgbCameraController(1920, 1080) as rgb_camera:
                rgb_camera.capture_image("/data/img", 90, ImageFormat.PNG)

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

    def __save_measurement(self, measurement: Measurement) -> Measurement:
        self.db.add(measurement)
        self.db.commit()
        self.db.refresh(measurement)

        return measurement
