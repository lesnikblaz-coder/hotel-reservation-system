import pytest

from datetime import date, timedelta

from hotel_reservation_system import repository

from hotel_reservation_system.services import reservation_services, guest_services, room_services

def get_future_dates(days_from_now=5, duration=7):
    check_in = date.today() + timedelta(days=days_from_now)
    check_out = check_in + timedelta(days=duration)
    return check_in.isoformat(), check_out.isoformat() #this returns check_in and check_out as default strings

def test_parse_date():
    date_ = reservation_services.parse_date("2026-05-21")

    assert date_ == date(2026, 5, 21)

    with pytest.raises(ValueError):
        reservation_services.parse_date("2026-50-21")

def test_validate_reservation_dates():
    check_in, check_out = get_future_dates()

    reservation_services.validate_reservation_dates(check_in, check_out)

    with pytest.raises(ValueError): # check-in after check-out
        reservation_services.validate_reservation_dates(check_out, check_in)

    with pytest.raises(ValueError): # past check in
        reservation_services.validate_reservation_dates("2026-04-21", "2026-04-30")

def test_reservation_create():
    # Arrange
    guest = guest_services.guest_create("Blob", "Balloon", "blob@gmail.com", "123456")
    room = room_services.room_create("single")
    check_in, check_out = get_future_dates()

    # Act
    reservation = reservation_services.reservation_create(guest.guest_id, room.room_id, check_in, check_out)

    # Assert
    assert reservation.reservation_id is not None
    assert reservation.status == "booked"
    assert reservation.guest_id == guest.guest_id
    assert reservation.room_id == room.room_id

def test_reservation_double_booking():
    # Arrange
    guest = guest_services.guest_create("Blob", "Balloon", "blob@gmail.com", "123456")
    room = room_services.room_create("single")
    check_in, check_out = get_future_dates()

    # Act
    reservation_services.reservation_create(guest.guest_id, room.room_id, check_in, check_out)

    # Assert - same dates should fail
    with pytest.raises(ValueError):
        reservation_services.reservation_create(guest.guest_id, room.room_id, check_in, check_out)

def test_reservation_cancel():
    # Arrange
    guest = guest_services.guest_create("Blob", "Balloon", "blob@gmail.com", "123456")
    room = room_services.room_create("single")
    check_in, check_out = get_future_dates()
    reservation = reservation_services.reservation_create(guest.guest_id, room.room_id, check_in, check_out)

    # Act
    reservation_services.reservation_cancel(guest.guest_id, reservation)

    # Assert
    updated = repository.get_reservation_by_id(reservation.reservation_id)
    assert updated.status == "cancelled"

def test_reservation_cancel_already_cancelled():
    # Arrange
    guest = guest_services.guest_create("Blob", "Balloon", "blob@gmail.com", "123456")
    room = room_services.room_create("single")
    check_in, check_out = get_future_dates()
    reservation = reservation_services.reservation_create(guest.guest_id, room.room_id, check_in, check_out)
    reservation_services.reservation_cancel(guest.guest_id, reservation)

    # cancelling again should fail
    with pytest.raises(ValueError):
        reservation_services.reservation_cancel(guest.guest_id, reservation)

def test_reservation_check_in():
    # Arrange
    guest = guest_services.guest_create("Blob", "Balloon", "blob@gmail.com", "123456")
    room = room_services.room_create("single")
    _, check_out = get_future_dates()
    reservation = reservation_services.reservation_create(guest.guest_id, room.room_id, date.today().isoformat(), check_out)

    # Act
    reservation_services.reservation_check_in(reservation.reservation_id)

    # Assert
    updated = repository.get_reservation_by_id(reservation.reservation_id)
    assert updated.status == "checked_in"

def test_reservation_check_out():
    # Arrange
    guest = guest_services.guest_create("Blob", "Balloon", "blob@gmail.com", "1234456")
    room = room_services.room_create("double")
    _, check_out = get_future_dates()
    reservation = reservation_services.reservation_create(guest.guest_id, room.room_id, date.today().isoformat(), check_out)
    reservation_services.reservation_check_in(reservation.reservation_id)

    # Act
    reservation_services.reservation_check_out(reservation.reservation_id)

    # Assert
    updated = repository.get_reservation_by_id(reservation.reservation_id)
    assert updated.status == "checked_out"