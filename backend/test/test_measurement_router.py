import datetime

from fastapi.testclient import TestClient
from datetime import datetime as dt, timezone

from measurement.model import Measurement, MeasurementState
from test_fixture import client_fixture, db_session_fixture, prepopulate_db, \
    sensor_settings  # import fixtures so pytest can use them
from time_machine import TimeMachineFixture
from sqlalchemy.orm import Session

AUTH = ("api", "changeit")

def test_list_measurements(client: TestClient, session: Session):
    # given
    prepopulate_db(dt(2018, 10, 5, 10, 0, 0), session)

    # when
    response = client.get("/measurement", auth=AUTH)

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
    response = client.get("/measurement/1", auth=AUTH)

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
    response = client.get("/measurement/558", auth=AUTH)

    # then
    assert response.status_code == 404


def test_create_measurement(time_machine: TimeMachineFixture, client: TestClient):
    # mock_time = dt(2015, 10, 21, 7, 28, 0, tzinfo=ZoneInfo("Europe/Prague"))

    # given
    # time_machine.move_to(destination=mock_time)
    request = {
        "name": "testing_measurement",
        "description": "testing_measurement",
        "duration": "PT10M",
        "sensor_settings": sensor_settings
    }

    # when
    response = client.post("/measurement", json=request, auth=AUTH)

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
        "duration": "PT10M",
        "ae_delta": "PT3M",
        "sensor_settings": sensor_settings
    }

    # when
    client.post("/measurement", json=request, auth=AUTH)

    # then
    result = session.query(Measurement).filter(Measurement.id == 1).first()
    assert result is not None
    assert result.name == "testing_measurement"
    assert result.description == "testing_measurement"
    assert result.planned_at == dt.fromisoformat("2015-10-23T07:00:00.000")
    assert result.ae_delta == datetime.timedelta(minutes=3)
    assert result.state == MeasurementState.PLANNED


def test_create_periodic_planned_measurement(time_machine: TimeMachineFixture, client: TestClient, session: Session):
    # given
    time_machine.move_to(dt(2015, 10, 21, 7, 0, 0))

    # when
    request = {
        "name": "Periodic measurement",
        "description": "testing measurement",
        "plan_from": "2015-10-23T08:00:00.000",
        "plan_to": "2015-10-23T10:30:00.000",
        "duration": "PT30M",
        "ae_delta": "PT1M",
        "sensor_settings": sensor_settings
    }
    client.post("/measurement/periodic", json=request, auth=AUTH)

    # then
    result = session.query(Measurement).all()
    assert len(result) == 6
    assert result[0].planned_at == dt(2015, 10, 23, 8, 0, 0)
    assert result[1].planned_at == dt(2015, 10, 23, 8, 30, 0)
    assert result[2].planned_at == dt(2015, 10, 23, 9, 0, 0)
    assert result[3].planned_at == dt(2015, 10, 23, 9, 30, 0)
    assert result[4].planned_at == dt(2015, 10, 23, 10, 0, 0)
    assert result[5].planned_at == dt(2015, 10, 23, 10, 30, 0)


def test_update_measurement(time_machine: TimeMachineFixture, client: TestClient, session: Session):
    # given
    time_machine.move_to(dt(2018, 10, 3, 10, 0, 0))
    prepopulate_db(dt(2018, 10, 5, 10, 0, 0), session)

    # when
    request = {
        "name": "updating",
        "description": "updating",
    }
    response = client.put("/measurement/1", json=request, auth=AUTH)

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
    response = client.put("/measurement/42", json=request, auth=AUTH)

    # then
    assert response.status_code == 404


def test_delete_measurement(time_machine: TimeMachineFixture, client: TestClient, session: Session):
    # given
    time_machine.move_to(dt(2018, 10, 3, 10, 0, 0))
    prepopulate_db(dt(2018, 10, 5, 10, 0, 0), session)

    # when
    response = client.delete("/measurement/1", auth=AUTH)

    # then
    assert response.status_code == 204


def test_delete_non_existing_measurement(client: TestClient):
    # given

    # when
    response = client.delete("/measurement/42", auth=AUTH)

    # then
    assert response.status_code == 204


def test_plan_measurement(time_machine: TimeMachineFixture, client: TestClient, session: Session):
    # given
    time_machine.move_to(dt(2018, 10, 23, 9, 0, 0))
    prepopulate_db(dt(2018, 10, 23, 9, 0, 0), session)

    # when
    request = {
        "plan_at": "2018-10-23T12:00:00.000",
        "ae_delta": "PT3M"
    }
    response = client.post("/measurement/1/plan", json=request, auth=AUTH)

    # then
    assert response.status_code == 200
    result = session.query(Measurement).filter(Measurement.id == 1).first()
    result.state = MeasurementState.PLANNED
    result.planned_at = dt(2018, 10, 23, 9, 0, 0)


def test_unplan_measurement(time_machine: TimeMachineFixture, client: TestClient, session: Session):
    # given
    time_machine.move_to(dt(2018, 10, 23, 9, 0, 0))
    prepopulate_db(dt(2018, 10, 23, 9, 0, 0), session)

    # when
    response = client.delete("/measurement/2/plan", auth=AUTH)

    # then
    assert response.status_code == 200
    result = session.query(Measurement).filter(Measurement.id == 2).first()
    assert result.state == MeasurementState.NEW
    assert result.planned_at is None
