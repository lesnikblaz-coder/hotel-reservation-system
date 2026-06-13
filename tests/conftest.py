import pytest
import os

from datetime import date, timedelta
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from database import Base, get_db
from api import app
from models import User
from auth import get_current_user

load_dotenv()

TEST_DATABASE_URL = (f'postgresql+psycopg2://'
                f'{os.getenv("DB_USER")}:'
                f'{os.getenv("DB_PASSWORD")}@'
                f'{os.getenv("DB_HOST")}:'
                f'{os.getenv("DB_PORT")}/'
                'hotel_system_test') # changed to the test database

engine_test = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine_test)
    yield
    Base.metadata.drop_all(bind=engine_test)

@pytest.fixture()
def test_db():
    connection = engine_test.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture()
def client(test_db):
    def override_get_db():
        yield test_db

    def override_auth():
        return User(user_id=1, email="testuser@user.com", role="admin", is_active=True)

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_auth

    yield TestClient(app)

    app.dependency_overrides.clear()

@pytest.fixture()
def create_guest(client):
    payload = {
        "first_name": "Storm",
        "last_name": "Test",
        "email": "storm@test.com",
        "phone": "123456"
    }

    response = client.post("/guests", json=payload)
    assert response.status_code == 201
    return response.json()

@pytest.fixture()
def create_room(client):
    payload = {
        "room_type": "double",
        "room_number": 201
    }

    response = client.post("/rooms", json=payload)
    assert response.status_code == 201
    return response.json()

@pytest.fixture()
def create_reservation(client, create_guest, create_room):
    payload = {
        "guest_id": create_guest["guest_id"],
        "room_id": create_room["room_id"],
        "check_in_date": date.today().isoformat(),
        "check_out_date": (date.today() + timedelta(days=7)).isoformat()
    }

    response = client.post("/reservations", json=payload)
    assert response.status_code == 201
    return response.json()