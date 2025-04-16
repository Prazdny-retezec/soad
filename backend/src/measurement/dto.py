from pydantic import BaseModel
from datetime import datetime, timedelta

from measurement.model import MeasurementState, MeasurementResult


class MeasurementResultDto(BaseModel):
    cloud_url: str | None = None
    error: str | None = None


class MeasurementCreateDto(BaseModel):
    name: str
    description: str
    plan_at: datetime | None = None
    ae_delta: timedelta = timedelta(minutes=3)

    class Config:
        to_attributes = True


class MeasurementCreatePeriodicDto(BaseModel):
    name: str
    description: str
    plan_from: datetime | None = None
    plan_to: datetime | None = None
    period: timedelta | None = None
    ae_delta: timedelta | None = None

    class Config:
        to_attributes = True


class MeasurementUpdateDto(BaseModel):
    name: str
    description: str


class MeasurementDetailDto(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime | None
    name: str
    description: str | None
    planned_at: datetime | None = None
    started_at: datetime | None = None
    ended_at: datetime | None = None
    state: MeasurementState
    result: MeasurementResultDto | None = None


class MeasurementListDto(BaseModel):
    id: int
    name: str
    description: str | None
    created_at: datetime
    planned_at: datetime | None = None
    state: MeasurementState

    class Config:
        from_attributes = True


class MeasurementPlanDto(BaseModel):
    plan_at: datetime | None = None
    ae_delta: timedelta | None = None
