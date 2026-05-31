from datetime import date

import repository

from exceptions import RoomNotFoundError, ReservationNotFoundError, InvalidDateFormatError, ConflictingDateError, \
    GuestNotFoundError

from models import Reservation
from services import guest_services


def parse_date(date_str: str) -> date:
    try:
        return date.fromisoformat(date_str) # expects "YYYY-MM-DD"
    except ValueError:
        raise InvalidDateFormatError(f'Invalid date format: "{date_str}". Use YYYY-MM-DD.')

def validate_reservation_dates(check_in: date, check_out: date):
    ci = check_in
    co = check_out

    if co <= ci:
        raise ConflictingDateError("Check-out must be after check-in.")
    if ci < date.today():
        raise ConflictingDateError("Check-in cannot be in the past.")

def reservation_create(guest_id: int, room_id: int, check_in_date: date, check_out_date: date):
    if not repository.get_guest_by_id(guest_id):
        raise GuestNotFoundError("Invalid guest ID.")

    if not repository.get_room_by_id(room_id):
        raise RoomNotFoundError("Invalid room ID.")

    validate_reservation_dates(check_in_date, check_out_date)

    #check if the room is already booked on those dates.
    conflict = repository.get_conflicting_reservations(room_id, check_in_date, check_out_date)

    if conflict:
        raise ConflictingDateError("Room already booked for that date.")

    reservation = Reservation(guest_id=guest_id, room_id=room_id, check_in_date=check_in_date, check_out_date=check_out_date, status="booked")
    new_reservation_id = repository.reservation_create(reservation)
    reservation.reservation_id = new_reservation_id
    return reservation

def reservation_select_by_id(reservation_id):
    reservation = repository.get_reservation_by_id(reservation_id)

    if not reservation:
        raise ReservationNotFoundError("Reservation doesn't exist.")

    return reservation

def reservation_price(reservation_id):
    reservation = reservation_select_by_id(reservation_id)

    room = repository.get_room_by_id(reservation.room_id)

    if room is None:
        raise RoomNotFoundError("Error: Room is None.")

    return room.total_price(reservation.duration_nights())

def reservation_cancel(reservation_id: int):
    reservation = reservation_select_by_id(reservation_id)
    reservation.cancel()
    repository.reservation_update(reservation.reservation_id, "status", reservation.status)

    return reservation

def reservation_check_in(reservation_id: int):
    reservation = reservation_select_by_id(reservation_id)
    reservation.check_in()
    repository.reservation_update(reservation_id, "status", reservation.status)

    return reservation

def reservation_check_out(reservation_id):
    reservation = reservation_select_by_id(reservation_id)
    reservation.check_out()
    repository.reservation_update(reservation_id, "status", reservation.status)

    return reservation

def reservations_get_all():
    reservations = repository.get_all_reservations()

    if not reservations:
        raise ReservationNotFoundError("No reservations found.")

    return reservations

def reservations_search_by_guest(guest_id):
    guest = guest_services.guest_select_by_id(guest_id)

    reservations = repository.get_reservation_by_guest(guest.guest_id)

    if not reservations:
        raise ReservationNotFoundError("Guest has no reservations.")

    return reservations