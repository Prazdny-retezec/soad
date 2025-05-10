from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Interval
from sqlalchemy.orm import relationship
from enum import StrEnum

from common.model import Auditable


class MeasurementState(StrEnum):
    NEW = "NEW",
    PLANNED = "PLANNED",
    DOWNLOADING = "DOWNLOADING",
    ZIPPING = "ZIPPING",
    UPLOADING = "UPLOADING",
    ERROR = "ERROR",
    FINISHED = "FINISHED",


class MeasurementResult(Auditable):
    __tablename__ = "measurement_result"

    # columns
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cloud_url = Column(String, nullable=True)
    error = Column(String, nullable=True)
    measurement_id = Column(Integer, ForeignKey("measurement.id"))

    # relationships
    measurement = relationship("Measurement", back_populates="result")


class Measurement(Auditable):
    __tablename__ = "measurement"

    # columns
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    planned_at = Column(DateTime, nullable=True)
    duration = Column(Interval)
    ae_delta = Column(Interval)
    started_at = Column(DateTime, nullable=True)
    ended_at = Column(DateTime, nullable=True)
    state = Column(Enum(MeasurementState), default=MeasurementState.NEW)
    scheduler_job_id = Column(String, nullable=True)

    # relationships
    result = relationship("MeasurementResult", back_populates="measurement", uselist=False, cascade="all, delete-orphan")
    sensor_settings = relationship("SensorSettings", back_populates="measurement", uselist=False, cascade="all, delete-orphan")
