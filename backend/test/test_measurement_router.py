import datetime

from fastapi.testclient import TestClient
from datetime import datetime as dt, timezone

from measurement.model import Measurement, MeasurementState
from test_fixture import client_fixture, db_session_fixture, prepopulate_db  # import fixtures so pytest can use them
from time_machine import TimeMachineFixture
from sqlalchemy.orm import Session


def test_list_measurements(client: TestClient, session: Session):
    # given
    prepopulate_db(dt(2018, 10, 5, 10, 0, 0), session)

    # when
    response = client.get("/measurement")

    # then
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 10
    assert data[0]["name"] == "Measurement 1"


def test_get_detail_measurement(time_machine: TimeMachineFixture, client: TestClient, session: Session):
    # given
    time_machine.move_to(dt(2018, 10, 3, 10, 0, 0))
    prepopulate_db(dt(2018, 10, 5, 10, 0, 0), session)

    # when
    response = client.get("/measurement/1")

    # then
    data = response.json()
    assert response.status_code == 200
    assert data["name"] == "Measurement 1"
    assert data["description"] == "Description of measurement 1"
    assert data["state"] == "NEW"
    assert data["created_at"] == "2018-10-03T12:00:00"  # TODO fix timezone shift (+2 hours wtf)
    assert data["planned_at"] is None
    assert data["started_at"] is None
    assert data["ended_at"] is None


def test_get_detail_non_existing_measurement(time_machine: TimeMachineFixture, client: TestClient, session: Session):
    # given
    time_machine.move_to(dt(2018, 10, 3, 10, 0, 0))
    prepopulate_db(dt(2018, 10, 5, 10, 0, 0), session)

    # when
    response = client.get("/measurement/558")

    # then
    assert response.status_code == 404


def test_create_measurement(time_machine: TimeMachineFixture, client: TestClient):
    # mock_time = dt(2015, 10, 21, 7, 28, 0, tzinfo=ZoneInfo("Europe/Prague"))

    # given
    # time_machine.move_to(destination=mock_time)
    request = {
        "name": "testing_measurement",
        "description": "testing_measurement",
    }

    # when
    response = client.post("/measurement", json=request)

    # then
    data = response.json()
    assert response.status_code == 201

    assert data["id"] == 1
    assert data["name"] == "testing_measurement"
    # assert dt.fromisoformat(data["created_at"]).isoformat() == mock_time.isoformat()
    assert data["state"] == "NEW"
    assert data["planned_at"] is None


def test_create_planned_measurement(time_machine: TimeMachineFixture, client: TestClient, session: Session):
    # given
    time_machine.move_to(dt(2015, 10, 21, 7, 28, 0))
    request = {
        "name": "testing_measurement",
        "description": "testing_measurement",
        "plan_at": "2015-10-23T07:00:00.000",
        "ae_delta": "PT3M"
    }

    # when
    client.post("/measurement", json=request)

    # then
    result = session.query(Measurement).filter(Measurement.id == 1).first()
    assert result is not None
    assert result.name == "testing_measurement"
    assert result.description == "testing_measurement"
    assert result.planned_at == dt.fromisoformat("2015-10-23T07:00:00.000")
    assert result.ae_delta == datetime.timedelta(minutes=3)
    assert result.state == MeasurementState.PLANNED


def test_update_measurement(time_machine: TimeMachineFixture, client: TestClient, session: Session):
    # given
    time_machine.move_to(dt(2018, 10, 3, 10, 0, 0))
    prepopulate_db(dt(2018, 10, 5, 10, 0, 0), session)

    # when
    request = {
        "name": "updating",
        "description": "updating",
    }
    response = client.put("/measurement/1", json=request)

    data = response.json()
    assert response.status_code == 202
    assert data["id"] == 1
    assert data["name"] == "updating"


def test_update_non_existing_measurement(time_machine: TimeMachineFixture, client: TestClient, session: Session):
    # given

    # when
    request = {
        "name": "updating",
        "description": "updating",
    }
    response = client.put("/measurement/42", json=request)

    # then
    assert response.status_code == 404


def test_delete_measurement(time_machine: TimeMachineFixture, client: TestClient, session: Session):
    # given
    time_machine.move_to(dt(2018, 10, 3, 10, 0, 0))
    prepopulate_db(dt(2018, 10, 5, 10, 0, 0), session)

    # when
    response = client.delete("/measurement/1")

    # then
    assert response.status_code == 204


def test_delete_non_existing_measurement(client: TestClient):
    # given

    # when
    response = client.delete("/measurement/42")

    # then
    assert response.status_code == 204
