from datetime import date
from sqlalchemy.orm import Session

import repository

from exceptions import RoomNotFoundError, ReservationNotFoundError, ConflictingDateError, GuestNotFoundError

from models import Reservation

def validate_reservation_dates(check_in: date, check_out: date):
    ci = check_in
    co = check_out

    if co <= ci:
        raise ConflictingDateError("Check-out must be after check-in.")
    if ci < date.today():
        raise ConflictingDateError("Check-in cannot be in the past.")

def reservation_create(db: Session, guest_id: int, room_id: int, check_in_date: date, check_out_date: date) -> Reservation:
    # check guest existence
    if not repository.get_guest_by_id(db, guest_id):
        raise GuestNotFoundError("Invalid guest ID.")

    # check room existence
    if not repository.get_room_by_id(db, room_id):
        raise RoomNotFoundError("Invalid room ID.")

    # validate dates
    validate_reservation_dates(check_in_date, check_out_date)

    # check if the room is already booked on those dates.
    conflict = repository.get_conflicting_reservations(db, room_id, check_in_date, check_out_date)

    if conflict:
        raise ConflictingDateError("Room already booked for that date.")

    # create a reservation with default status "booked"
    reservation = Reservation(guest_id=guest_id, room_id=room_id, check_in_date=check_in_date, check_out_date=check_out_date, status="booked")

    return repository.reservation_create(db, reservation)

def reservation_select_by_id(db: Session, reservation_id: int) -> Reservation:
    reservation = repository.get_reservation_by_id(db, reservation_id)

    if not reservation:
        raise ReservationNotFoundError("Reservation doesn't exist.")

    return reservation

def reservation_price(db: Session, reservation_id: int) -> float:
    reservation = reservation_select_by_id(db, reservation_id)

    room = repository.get_room_by_id(db, reservation.room_id)

    if room is None:
        raise RoomNotFoundError("Error: Room is None.")

    return room.total_price(reservation.duration_nights())

def reservation_cancel(db: Session, reservation_id: int) -> Reservation:
    reservation = reservation_select_by_id(db, reservation_id)
    reservation.cancel()

    return repository.reservation_save(db, reservation)

def reservation_check_in(db: Session, reservation_id: int) -> Reservation:
    reservation = reservation_select_by_id(db, reservation_id)
    reservation.check_in()

    return repository.reservation_save(db, reservation)

def reservation_check_out(db: Session, reservation_id: int) -> Reservation:
    reservation = reservation_select_by_id(db, reservation_id)
    reservation.check_out()

    return repository.reservation_save(db, reservation)

def reservations_get_all(db: Session) -> list[Reservation]:
    return repository.get_all_reservations(db)

def reservations_search_by_guest(db: Session, guest_id: int) -> list[Reservation]:
    # checks if guest exists
    repository.get_guest_by_id(db, guest_id)

    reservations = repository.get_reservation_by_guest(db, guest_id)

    if not reservations:
        raise ReservationNotFoundError("Guest has no reservations.")

    return reservations