from datetime import datetime
from typing import List

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException

from database import get_db
from measurement.dto import MeasurementCreateDto, MeasurementUpdateDto
from measurement.model import Measurement, MeasurementState


class MeasurementService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

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
                 .order_by(Measurement.planned_from.asc())
        )

        entities = query.all()
        return entities

    def create_measurement(self, dto: MeasurementCreateDto) -> Measurement:
        # map DTO to entity
        entity = Measurement(
            name=dto.name,
            planned_from=dto.planned_from,
            planned_to=dto.planned_to,
            state=MeasurementState.NEW,
        )

        # validation
        self.__pre_persist_validation(entity)

        # save entity in database
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)

        return entity

    def update_measurement(self, measurement_id: int, dto: MeasurementUpdateDto) -> Measurement:
        old_entity = self.get_measurement(measurement_id)

        # map DTO to entity
        new_entity = old_entity
        new_entity.name = dto.name
        new_entity.planned_from = dto.planned_from
        new_entity.planned_to = dto.planned_to
        new_entity.state = dto.state

        # validation
        self.__pre_persist_validation(new_entity)

        # update entity in database
        self.db.add(new_entity)
        self.db.commit()
        self.db.refresh(new_entity)

        return new_entity

    def delete_measurement(self, measurement_id: int):
        query = (self.db
            .query(Measurement)
            .filter(
                (Measurement.id == measurement_id) &
                (Measurement.deleted_at.is_(None))
            )
        )

        entity = query.first()
        if entity is not None:
            entity.deleted_at = datetime.now()
            self.db.add(entity)
            self.db.commit()

    @staticmethod
    def __pre_persist_validation(measurement: Measurement):
        # TODO validation - implement me
        if measurement.planned_from > measurement.planned_to:
            raise ValueError("planned_from must be before planned_to")
