from sqlalchemy import select

import pytest

from exceptions import NoChangesError
from models import Room
from constants import VALID_ROOM_TYPES

def test_create_room(client, test_db):
    response = client.post("/rooms", json={
        "room_type": "double",
        "room_number": 201
    })

    assert response.status_code == 201

    room_id = response.json()["room_id"]
    room = test_db.scalar(select(Room).where(Room.room_id == room_id))

    assert room is not None
    assert room.room_id is not None
    assert room.room_type == "double"
    assert room.room_number == 201
    assert room.capacity == VALID_ROOM_TYPES["double"]["capacity"]
    assert room.price_per_night == VALID_ROOM_TYPES["double"]["price_per_night"]
    assert room.is_active == True

def test_invalid_room(client):
    response = client.post("/rooms", json={
        "room_type": "invalid",
        "room_number": 201
    })
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Input should be 'single', 'double' or 'suite'"

def test_missing_field_room(client):
    response = client.post("/rooms", json={
        "room_type": "suite"
    })
    assert response.status_code == 422

def test_invalid_room_number(client):
    response = client.post("/rooms", json={
        "room_type": "suite",
        "room_number": -100
    })
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Value error, Room number must be positive."

def test_duplicate_room_numbers(client, create_room):
    room1 = create_room
    response = client.post("/rooms", json={
        "room_type": "single",
        "room_number": room1["room_number"]
    })
    assert response.status_code == 409
    assert response.json()["detail"] == "Room number already exists."

def test_total_price(create_room, test_db):
    room_id = create_room["room_id"]
    room = test_db.scalar(select(Room).where(Room.room_id == room_id))

    nights = 7

    total_price = room.total_price(nights)
    correct_ans = room.price_per_night * nights

    assert total_price == correct_ans

def test_get_rooms(client, create_room):
    response = client.get("/rooms")
    assert response.status_code == 200

    data = response.json()
    assert data[0]["room_id"] == create_room["room_id"]

def test_get_available_rooms(client, create_guest, create_room, create_reservation):
    # must create_guest and create_room so the IDs are valid
    reservation = create_reservation

    response = client.post("/rooms/availability", json={
        "check_in_date": "2026-09-10", # dates must be in the future
        "check_out_date": "2026-09-17"
    })
    assert response.status_code == 200

    # must fail because of conflicting dates meaning no available rooms at that time
    response_404 = client.post("/rooms/availability", json={
        "check_in_date": reservation["check_in_date"],
        "check_out_date": reservation["check_out_date"]
    })
    assert response_404.status_code == 404

def test_get_room_id(client, create_room):
    room_id = create_room["room_id"]
    response = client.get(f"/rooms/{room_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["room_id"] == room_id

def test_get_nonexistent_room(client):
    response = client.get(f"/rooms/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Room not found."

def test_update_room(client, create_room):
    room_id = create_room["room_id"]
    response = client.put(f"/rooms/{room_id}", json={
        "price_per_night": 999.99
    })

    assert response.status_code == 200
    assert response.json()["price_per_night"] == 999.99

def test_invalid_update(client, create_room):
    room_id = create_room["room_id"]
    response = client.put(f"/rooms/{room_id}", json={
        "capacity": 0
    })
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Input should be greater than or equal to 2"

def test_delete_room(client, create_room, test_db):
    room_id = create_room["room_id"]
    response = client.delete(f"/rooms/{room_id}")
    assert response.status_code == 204

    room = test_db.scalar(select(Room).where(Room.room_id == room_id))
    assert room is None

def test_activate_room(client, create_room, test_db):
    room_id = create_room["room_id"]
    room = test_db.scalar(select(Room).where(Room.room_id == room_id))
    room.is_active = False # make room inactive
    assert room is not None

    room.activate()
    assert room.is_active == True

def test_deactivate_room(client, create_room, test_db):
    room_id = create_room["room_id"]
    room = test_db.scalar(select(Room).where(Room.room_id == room_id))
    assert room is not None

    room.deactivate()
    assert room.is_active == False

def test_activate_already_active_room(client, create_room, test_db):
    room_id = create_room["room_id"]
    room = test_db.scalar(select(Room).where(Room.room_id == room_id))
    assert room is not None

    with pytest.raises(NoChangesError):
        room.activate()

def test_deactivate_already_inactive_room(client, create_room, test_db):
    room_id = create_room["room_id"]
    room = test_db.scalar(select(Room).where(Room.room_id == room_id))
    room.is_active = False  # make room inactive
    test_db.commit()

    assert room is not None

    with pytest.raises(NoChangesError):
        room.deactivate()