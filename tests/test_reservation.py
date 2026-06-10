from datetime import date, timedelta
from sqlalchemy import select

from models import Reservation

import enums

def test_reservation_create(client, test_db, create_guest, create_room):
    response = client.post("/reservations", json={
        "guest_id": create_guest["guest_id"],
        "room_id": create_room["room_id"],
        "check_in_date": date.today().isoformat(),
        "check_out_date": (date.today() + timedelta(days=7)).isoformat()
    })

    assert response.status_code == 201

    reservation_id = response.json()["reservation_id"]
    reservation = test_db.scalar(select(Reservation).where(Reservation.reservation_id == reservation_id))

    assert reservation is not None
    assert reservation.reservation_id is not None
    assert reservation.guest_id is not None
    assert reservation.room_id is not None
    assert reservation.check_in_date == date.today()
    assert reservation.check_out_date == date.today() + timedelta(days=7)
    assert reservation.status == enums.ReservationStatus.BOOKED
    assert reservation.total_price is not None

def test_invalid_guest_id_reservation(client, create_room):
    response = client.post("/reservations", json={
        "guest_id": 999999,
        "room_id": create_room["room_id"],
        "check_in_date": date.today().isoformat(),
        "check_out_date": (date.today() + timedelta(days=7)).isoformat()
    })

    assert response.status_code == 404
    assert response.json()["detail"] == "Invalid guest ID."

def test_invalid_room_id_reservation(client, create_guest):
    response = client.post("/reservations", json={
        "guest_id": create_guest["guest_id"],
        "room_id": 999999,
        "check_in_date": date.today().isoformat(),
        "check_out_date": (date.today() + timedelta(days=7)).isoformat()
    })

    assert response.status_code == 404
    assert response.json()["detail"] == "Invalid room ID."

def test_invalid_check_out(client, create_guest, create_room):
    response = client.post("/reservations", json={
        "guest_id": create_guest["guest_id"],
        "room_id": create_room["room_id"],
        "check_in_date": date.today().isoformat(),
        "check_out_date": (date.today() + timedelta(days=-7)).isoformat()
    })

    assert response.status_code == 409
    assert response.json()["detail"] == "Check-out must be after check in."

def test_conflicting_dates(client, create_reservation, create_room, create_guest):
    response = client.post("/reservations", json={
        "guest_id": create_guest["guest_id"],
        "room_id": create_room["room_id"],
        "check_in_date": date.today().isoformat(),
        "check_out_date": (date.today() + timedelta(days=7)).isoformat()
    })

    assert response.status_code == 409
    assert response.json()["detail"] == "Room already booked for that date."

def test_get_reservations(client, create_reservation):
    response = client.get("/reservations")
    assert response.status_code == 200

    data = response.json()
    assert data[0]["reservation_id"] == create_reservation["reservation_id"]

def test_get_reservation_id(client, create_reservation):
    reservation_id = create_reservation["reservation_id"]
    response = client.get(f"/reservations/{reservation_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["reservation_id"] == reservation_id

def test_update_reservation(client, create_reservation):
    reservation_id = create_reservation["reservation_id"]

    response = client.put(f"/reservations/{reservation_id}", json={
        "check_in_date": (date.today() + timedelta(days=2)).isoformat(),
        "check_out_date": (date.today() + timedelta(days=9)).isoformat()
    })

    assert response.status_code == 200
    assert response.json()["check_in_date"] is not None
    assert response.json()["check_out_date"] is not None

def test_cancel_reservation(client, create_reservation):
    reservation_id = create_reservation["reservation_id"]

    response = client.post(f"/reservations/{reservation_id}/cancel")

    assert response.status_code == 200
    assert response.json()["status"] == enums.ReservationStatus.CANCELLED

def test_invalid_cancel_reservation(client, create_reservation, test_db):
    reservation_id = create_reservation["reservation_id"]
    reservation = test_db.scalar(select(Reservation).where(Reservation.reservation_id == reservation_id))
    reservation.status = enums.ReservationStatus.CHECKED_IN  # make reservation's status "checked_in" for invalid cancel
    test_db.commit()

    response = client.post(f"/reservations/{reservation.reservation_id}/cancel")

    assert response.status_code == 409
    assert response.json()["detail"] == "Only booked reservations can be cancelled."

def test_check_in_reservation(client, create_reservation):
    reservation_id = create_reservation["reservation_id"]

    response = client.post(f"/reservations/{reservation_id}/check-in")

    assert response.status_code == 200
    assert response.json()["status"] == enums.ReservationStatus.CHECKED_IN

def test_invalid_check_in_date(client, create_reservation, test_db):
    reservation_id = create_reservation["reservation_id"]
    reservation = test_db.scalar(select(Reservation).where(Reservation.reservation_id == reservation_id))
    reservation.check_in_date = (date.today() + timedelta(days=2))  # make reservation's check in date > today's date for unallowed check in
    test_db.commit()

    response = client.post(f"/reservations/{reservation.reservation_id}/check-in")

    assert response.status_code == 422
    assert response.json()["detail"] == f"Check-in allowed only on {reservation.check_in_date}"

def test_invalid_check_in_status(client, create_reservation, test_db):
    reservation_id = create_reservation["reservation_id"]
    reservation = test_db.scalar(select(Reservation).where(Reservation.reservation_id == reservation_id))
    reservation.status = enums.ReservationStatus.CHECKED_OUT  # make reservation's status "checked_out" for invalid check in
    test_db.commit()

    response = client.post(f"/reservations/{reservation.reservation_id}/check-in")

    assert response.status_code == 409
    assert response.json()["detail"] == "Only booked reservations can be checked in."

def test_check_out_reservation(client, create_reservation, test_db):
    reservation_id = create_reservation["reservation_id"]
    reservation = test_db.scalar(select(Reservation).where(Reservation.reservation_id == reservation_id))
    reservation.status = enums.ReservationStatus.CHECKED_IN # make reservation's status "checked_in" for allowed check out
    test_db.commit()

    response = client.post(f"/reservations/{reservation.reservation_id}/check-out")

    assert response.status_code == 200
    assert response.json()["status"] == enums.ReservationStatus.CHECKED_OUT

def test_invalid_check_out_reservation(client, create_reservation):
    reservation_id = create_reservation["reservation_id"]

    response = client.post(f"/reservations/{reservation_id}/check-out")

    assert response.status_code == 409
    assert response.json()["detail"] == "Only checked-in reservations can be checked out."

def test_duration_nights(client, create_reservation, test_db):
    reservation_id = create_reservation["reservation_id"] # created reservation's duration is 7 days
    reservation = test_db.scalar(select(Reservation).where(Reservation.reservation_id == reservation_id))

    assert reservation.duration_nights() == 7