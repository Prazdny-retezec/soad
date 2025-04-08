from pydantic import BaseModel
from datetime import datetime, timedelta

from measurement.model import MeasurementState


class MeasurementCreateDto(BaseModel):
    name: str
    description: str
    planned_from: datetime | None = None
    planned_to: datetime | None = None
    period: timedelta | None = None
    ae_delta: timedelta | None = None

    class Config:
        to_attributes = True


class MeasurementUpdateDto(BaseModel):
    name: str
    description: str
    planned_from: datetime
    planned_to: datetime
    state: MeasurementState


class MeasurementDetailDto(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime | None
    name: str
    description: str | None
    planned_from: datetime | None = None
    planned_to: datetime | None = None
    state: MeasurementState


class MeasurementListDto(BaseModel):
    id: int
    name: str
    created_at: datetime
    planned_from: datetime | None = None
    planned_to: datetime | None = None
    state: MeasurementState

    class Config:
        from_attributes = True
