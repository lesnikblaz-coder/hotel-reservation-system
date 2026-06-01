import pytest

from datetime import date, timedelta

from models import Reservation
from exceptions import InvalidReservationStateError, InvalidCheckInDateError

def test_cancel():
    reservation_booked = Reservation(
        status="booked"
    )

    reservation_booked.cancel()
    assert reservation_booked.status == "cancelled"

def test_cancel_invalid():
    reservation_checked_out = Reservation(
        status="checked_out"
    )
    reservation_checked_in = Reservation(
        status="checked_in"
    )
    reservation_cancelled = Reservation(
        status="cancelled"
    )

    with pytest.raises(InvalidReservationStateError):
        reservation_checked_out.cancel()

    with pytest.raises(InvalidReservationStateError):
        reservation_checked_in.cancel()

    with pytest.raises(InvalidReservationStateError):
        reservation_cancelled.cancel()

def test_check_in_success():
    reservation = Reservation(
        check_in_date=date.today(),
        check_out_date=date.today() + timedelta(days=7),
        status="booked"
    )

    reservation.check_in()

    assert reservation.status == "checked_in"

def test_check_in_wrong_day():
    reservation = Reservation(
        check_in_date=date.today() + timedelta(days=2),
        check_out_date=date.today() + timedelta(days=7),
        status="booked"
    )

    with pytest.raises(InvalidCheckInDateError):
        reservation.check_in()

def test_check_out_success():
    reservation = Reservation(
        status="checked_in",
        check_in_date=date.today() - timedelta(days=3),
        check_out_date=date.today()
    )

    reservation.check_out()

    assert reservation.status == "checked_out"

def test_check_out_invalid_state():
    reservation = Reservation(
        status="booked"
    )

    with pytest.raises(InvalidReservationStateError):
        reservation.check_out()

def test_duration_nights():
    reservation = Reservation(
        check_in_date=date(2026, 6, 1),
        check_out_date=date(2026, 6, 8),
        status="booked"
    )

    assert reservation.duration_nights() == 7