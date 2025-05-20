from pydantic import BaseModel
from datetime import datetime, timedelta

from measurement.model import MeasurementState
from sensor.dto import SensorSettingsDto


class MeasurementResultDto(BaseModel):
    cloud_url: str | None = None
    error: str | None = None


class MeasurementCreateDto(BaseModel):
    name: str
    description: str
    plan_at: datetime | None = None
    duration: timedelta = timedelta(minutes=10)
    ae_delta: timedelta = timedelta(minutes=3)
    sensor_settings: SensorSettingsDto = SensorSettingsDto()

    class Config:
        to_attributes = True


class MeasurementCreatePeriodicDto(BaseModel):
    name: str
    description: str
    plan_from: datetime | None = None
    plan_to: datetime | None = None
    duration: timedelta = timedelta(minutes=10)
    ae_delta: timedelta = timedelta(minutes=3)
    sensor_settings: SensorSettingsDto = SensorSettingsDto()

    class Config:
        to_attributes = True


class MeasurementUpdateDto(BaseModel):
    name: str
    description: str
    sensor_settings: SensorSettingsDto = SensorSettingsDto()


class MeasurementDetailDto(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime | None
    name: str
    description: str | None
    planned_at: datetime | None = None
    started_at: datetime | None = None
    ended_at: datetime | None = None
    ae_delta: timedelta
    duration: timedelta
    state: MeasurementState
    result: MeasurementResultDto | None = None
    sensor_settings: SensorSettingsDto

    class Config:
        from_attributes = True


class MeasurementListDto(BaseModel):
    id: int
    name: str
    description: str | None
    created_at: datetime
    planned_at: datetime | None = None
    state: MeasurementState
    duration: timedelta
    result: MeasurementResultDto | None = None

    class Config:
        from_attributes = True


class MeasurementPlanDto(BaseModel):
    plan_at: datetime | None = None
    ae_delta: timedelta | None = None
