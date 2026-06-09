import pytest
import os

from datetime import date, timedelta
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from database import Base, get_db
from api import app
from models import Guest

load_dotenv()

TEST_DATABASE_URL = (f'postgresql+psycopg2://'
                f'{os.getenv("DB_USER")}:'
                f'{os.getenv("DB_PASSWORD")}@'
                f'{os.getenv("DB_HOST")}:'
                f'{os.getenv("DB_PORT")}/'
                'hotel_system_test') # changed to the test database

engine_test = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine_test) #//// do sessions and transactions.

    test_db = TestingSessionLocal()
    try:
        yield test_db
    finally:
        test_db.close()

    Base.metadata.drop_all(bind=engine_test) #//// do sessions and transactions.

@pytest.fixture()
def client(test_db):
    def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

    app.dependency_overrides.clear()

@pytest.fixture()
def guest_payload():
    return {
        "first_name": "Storm",
        "last_name": "Test",
        "email": "storm@test.com",
        "phone": "123456"
    }

@pytest.fixture()
def room_payload():
    return {
        "room_type": "double",
        "room_number": 201
    }

@pytest.fixture()
def reservation_payload():
    check_in = date.today()

    return {
        "guest_id": 1,
        "room_id": 1,
        "check_in_date": check_in.isoformat(),
        "check_out_date": (check_in + timedelta(days=7)).isoformat()
    }

@pytest.fixture()
def create_guest(client, guest_payload):
    response = client.post("/guests", json=guest_payload)
    assert response.status_code == 201
    return response.json()

@pytest.fixture()
def create_room(client, room_payload):
    response = client.post("/rooms", json=room_payload)
    assert response.status_code == 201
    return response.json()

@pytest.fixture()
def create_reservation(client, reservation_payload):
    response = client.post("/reservations", json=reservation_payload)
    assert response.status_code == 201
    return response.json()