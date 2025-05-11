from datetime import datetime, timedelta

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from main import app
from database import Base, get_db
from measurement.model import Measurement, MeasurementState
from sensor.dto import SensorSettingsDto

sensor_settings = {
    "rgb_image_quality": 90,
    "rgb_image_count": 5,
    "rgb_image_width": 1920,
    "rgb_image_height": 1080,
    "rgb_sampling_delay": 2,
    "rgb_image_format": "TIFF",
    "ms_image_count": 2,
    "ms_image_width": 1920,
    "ms_image_height": 1080,
    "ms_sampling_delay": 5,
    "ms_image_format": "TIFF",
    "ae_voltage_format": 5,
    "ae_voltage_dbae": 1,
    "ae_counts_log": 1,
    "ae_counts_lin": 1,
    "ae_energy_format": 1
}


# for testing purposes create connection to SQLite database
@pytest.fixture(name="session")
def db_session_fixture():
    engine = create_engine(
        url="sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )

    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        yield session


# prepare client for testing (override dependencies of normal app)
@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_db_override():
        return session

    app.dependency_overrides[get_db] = get_db_override
    client = TestClient(app)

    yield client

    app.dependency_overrides.clear()


def prepopulate_db(base_date: datetime, session: Session):
    """Helper function to populate 10 measurement records in the database using static data."""
    static_data = [
        {"id": 1, "name": "Measurement 1", "description": "Description of measurement 1", "state": MeasurementState.NEW,
         "planned_at": None, "created_at": base_date + timedelta(days=1)},
        {"id": 2, "name": "Measurement 2", "description": "Description of measurement 2", "state": MeasurementState.PLANNED,
         "planned_at": base_date + timedelta(hours=2), "created_at": base_date + timedelta(days=2)},
        {"id": 3,"name": "Measurement 3", "description": "Description of measurement 3", "state": MeasurementState.DOWNLOADING,
         "planned_at": base_date + timedelta(days=3, hours=1), "created_at": base_date + timedelta(days=2)},
        {"id": 4, "name": "Measurement 4", "description": "Description of measurement 4", "state": MeasurementState.ZIPPING,
         "planned_at": base_date + timedelta(days=4), "created_at": base_date + timedelta(days=4)},
        {"id": 5, "name": "Measurement 5", "description": "Description of measurement 5", "state": MeasurementState.UPLOADING,
         "planned_at": base_date + timedelta(days=5), "created_at": base_date + timedelta(days=5)},
        {"id": 6, "name": "Measurement 6", "description": "Description of measurement 6", "state": MeasurementState.ERROR,
         "planned_at": base_date + timedelta(days=6), "created_at": base_date + timedelta(days=6)},
        {"id": 7, "name": "Measurement 7", "description": "Description of measurement 7", "state": MeasurementState.FINISHED,
         "planned_at": base_date + timedelta(days=7), "created_at": base_date + timedelta(days=7)},
        {"id": 8, "name": "Measurement 8", "description": "Description of measurement 8", "state": MeasurementState.NEW,
         "planned_at": base_date + timedelta(days=8), "created_at": base_date + timedelta(days=8)},
        {"id": 9,"name": "Measurement 9", "description": "Description of measurement 9", "state": MeasurementState.PLANNED,
         "planned_at": base_date + timedelta(days=9), "created_at": base_date + timedelta(days=9)},
        {"id": 10, "name": "Measurement 10", "description": "Description of measurement 10",
         "state": MeasurementState.DOWNLOADING, "planned_at": base_date + timedelta(days=10),
         "created_at": base_date + timedelta(days=10)},
    ]

    for measurement in static_data:
        # Použití cyklu pro statické záznamy
        started_at = None
        if measurement["state"] in ["DOWNLOADING", "ZIPPING", "UPLOADING", "FINISHED"]:
            started_at = measurement["planned_at"] + timedelta(seconds=2)

        ended_at = None
        if measurement["state"] in ["FINISHED"]:
            ended_at = measurement["planned_at"] + timedelta(minutes=3)

        measurement = Measurement(
            id=measurement["id"],
            name=measurement["name"],
            description=measurement["description"],
            planned_at=measurement["planned_at"],
            ae_delta=timedelta(minutes=5),
            started_at=started_at,
            ended_at=ended_at,
            state=measurement["state"],
            duration=timedelta(seconds=10),
            scheduler_job_id=None
        )
        measurement.sensor_settings = SensorSettingsDto(**sensor_settings).to_entity()
        session.add(measurement)

    session.commit()
