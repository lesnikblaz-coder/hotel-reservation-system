from sqlalchemy import select

from models import Guest

def test_create_guest(client, test_db):
    response = client.post("/guests", json={
            "first_name": "Storm",
            "last_name": "Test",
            "email": "storm@test.com",
            "phone": "123456"
        }
    )

    assert response.status_code == 201

    guest_id = response.json()["guest_id"]
    guest = (
        test_db.scalar(select(Guest).where(Guest.guest_id == guest_id))
    )

    assert guest is not None
    assert guest.guest_id is not None
    assert guest.first_name == "Storm"
    assert guest.last_name == "Test"
    assert guest.email == "storm@test.com"
    assert guest.phone == "123456"
    assert guest.full_name() == "Storm Test"

def test_invalid_email(client):
    response = client.post("/guests", json={
        "first_name": "Storm",
        "last_name": "Test",
        "email": "invalid-email-entry",
        "phone": "123456"
    })

    assert response.status_code == 422

def test_invalid_phone(client):
    response = client.post("/guests", json={
        "first_name": "Storm",
        "last_name": "Test",
        "email": "storm@test.com",
        "phone": "invalid-phone-entry"
    })

    assert response.status_code == 422

def test_missing_field_create_guest(client, test_db):
    response = client.post("/guests", json={
        "first_name": "Storm",
        "last_name": "Test"
    })

    assert response.status_code == 422

def test_get_guest(client, create_guest):
    response = client.get("/guests")
    assert response.status_code == 200

    data = response.json()
    assert data[0]["email"] == "storm@test.com"

def test_get_guest_id(client, create_guest):
    guest_id = create_guest["guest_id"]

    response = client.get(f"/guests/{guest_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["email"] == "storm@test.com"

def test_get_nonexistent_guest(client):
    response = client.get("/guests/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Guest does not exist."

def test_update_guest(client, create_guest):
    guest_id = create_guest["guest_id"]

    response = client.put(f"/guests/{guest_id}", json={
        "first_name": "StormUpdated",
        "last_name": "TestUpdated",
        "email": "storm@testupdating.com"
    })

    assert response.status_code == 200

    data = response.json()
    assert data["first_name"] == "StormUpdated"
    assert data["last_name"] == "TestUpdated"
    assert data["email"] == "storm@testupdating.com"
    assert data["phone"] == "123456"

def test_delete_guest(client, test_db, create_guest):
    guest_id = create_guest["guest_id"]

    response = client.delete(f"/guests/{guest_id}")
    assert response.status_code == 204

    deleted_guest = test_db.scalar(select(Guest).where(Guest.guest_id == guest_id))
    assert deleted_guest is None