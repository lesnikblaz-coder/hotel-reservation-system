import pytest

from datetime import date, timedelta

from hotel_reservation_system.services import guest_services, reservation_services, room_services
from hotel_reservation_system import repository


def test_guest_create():
    guest = guest_services.guest_create(
        "Blob",
        "Balloon",
        "blob.balloon@gmail.com",
        "123456"
    )

    loaded_guest = repository.get_guest_by_id(guest.guest_id)
    assert loaded_guest is not None

    assert loaded_guest.first_name == "Blob"
    assert loaded_guest.last_name == "Balloon"
    assert loaded_guest.email == "blob.balloon@gmail.com"
    assert loaded_guest.phone == "123456"

    # duplicate email should fail
    with pytest.raises(ValueError):
        guest_services.guest_create(
            "Nlob",
            "Nalloon",
            "blob.balloon@gmail.com",
            "1239552529"
        )

    # update test (use dynamic ID, NOT 1)
    guest_services.guest_update(guest, "first_name", "BLOBSKI")

    updated = repository.get_guest_by_id(guest.guest_id)

    assert updated is not None

    assert updated.first_name == "BLOBSKI"


def test_guest_select_by_id():
    guest = guest_services.guest_create(
        "Blob",
        "Balloon",
        "blob.balloon2@gmail.com",
        "999999"
    )

    result = guest_services.guest_select_by_id(guest.guest_id)

    assert result.guest_id == guest.guest_id
    assert result.email == "blob.balloon2@gmail.com"


def test_guest_select_invalid_id():
    with pytest.raises(ValueError):
        guest_services.guest_select_by_id(9999)

def fake_guest_room_reservation():
    guest = guest_services.guest_create("Blob", "Balloon", "blob@gmail.com", "123456")
    room = room_services.room_create("single")
    check_in = date.today().isoformat()
    check_out = (date.today() + timedelta(days=7)).isoformat()
    reservation = reservation_services.reservation_create(guest.guest_id, room.room_id, check_in, check_out)
    return guest, room, reservation

def test_guest_delete_booked():
    guest, room, reservation = fake_guest_room_reservation()

    with pytest.raises(ValueError): #status is booked
        guest_services.guest_delete(guest)

def test_guest_delete_checked_in():
    guest, room, reservation = fake_guest_room_reservation()

    reservation_services.reservation_check_in(reservation.reservation_id) # goes through service, updates DB

    with pytest.raises(ValueError): #status is checked_in
        guest_services.guest_delete(guest)

def test_guest_delete_checked_out():
    guest, room, reservation = fake_guest_room_reservation()

    reservation_services.reservation_check_in(reservation.reservation_id)
    reservation_services.reservation_check_out(reservation.reservation_id)

    guest_services.guest_delete(guest)

def test_guest_delete_cancelled():
    guest, room, reservation = fake_guest_room_reservation()

    reservation_services.reservation_cancel(guest.guest_id, reservation)

    guest_services.guest_delete(guest)