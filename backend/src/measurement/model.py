from sqlalchemy import Column, Integer, String, DateTime, Enum
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


class Measurement(Auditable):
    __tablename__ = "measurement"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String)
    planned_from = Column(DateTime)
    planned_to = Column(DateTime)
    state = Column(Enum(MeasurementState), nullable=False, default=MeasurementState.NEW)
