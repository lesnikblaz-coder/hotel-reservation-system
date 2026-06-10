from datetime import date
from sqlalchemy.orm import Session

import repository
import enums

from exceptions import RoomNotFoundError, ReservationNotFoundError, ConflictingDateError, GuestNotFoundError, InvalidReservationStateError
from schemas import ReservationUpdate
from models import Reservation, Room

def validate_reservation_dates(check_in_date: date, check_out_date: date):
    if check_out_date <= check_in_date:
        raise ConflictingDateError("Check-out must be after check-in.")
    if check_in_date < date.today():
        raise ConflictingDateError("Check-in cannot be in the past.")

def validate_guest_exists(db: Session, guest_id: int) -> None:
    if not repository.get_guest_by_id(db, guest_id):
        raise GuestNotFoundError("Invalid guest ID.")

def validate_room_exists(db: Session, room_id: int) -> Room:
    room = repository.get_room_by_id(db, room_id)

    if not room:
        raise RoomNotFoundError("Invalid room ID.")

    return room

def validate_room_availability(db: Session, room_id: int, check_in: date, check_out: date, exclude_reservation_id: int | None = None) -> None:
    conflict = repository.get_conflicting_reservations(db, room_id, check_in, check_out, exclude_reservation_id)
    if conflict:
        raise ConflictingDateError("Room already booked for that date.")

def reservation_create(db: Session, guest_id: int, room_id: int, check_in_date: date, check_out_date: date) -> Reservation:
    # check guest existence
    validate_guest_exists(db, guest_id)

    # check room existence
    room = validate_room_exists(db, room_id)

    # check if the room is already booked on those dates.
    validate_room_availability(db, room_id, check_in_date, check_out_date)

    # date validation
    validate_reservation_dates(check_in_date, check_out_date)

    # create a reservation with default status "booked"
    reservation = Reservation(guest_id=guest_id, room_id=room_id, check_in_date=check_in_date, check_out_date=check_out_date, status=enums.ReservationStatus.BOOKED.value)

    reservation.total_price = room.total_price(reservation.duration_nights())

    return repository.reservation_create(db, reservation)

def reservation_update(db: Session, reservation_id: int, data: ReservationUpdate) -> Reservation:
    reservation = reservation_select_by_id(db, reservation_id)

    # check guest existence if input
    if data.guest_id is not None:
        validate_guest_exists(db, data.guest_id)

    # check room existence if input
    if data.room_id is not None:
        validate_room_exists(db, data.room_id)

    if data.check_in_date is not None or data.check_out_date is not None:
        # if stay has started, cannot modify dates
        if reservation.check_in_date <= date.today() and reservation.status != enums.ReservationStatus.BOOKED:
            raise InvalidReservationStateError("Cannot modify dates after stay has started.")

        # if dates valid -> check if the room is already booked on those dates
        new_check_in = (data.check_in_date if data.check_in_date is not None else reservation.check_in_date)
        new_check_out = (data.check_out_date if data.check_out_date is not None else reservation.check_out_date)
        new_room_id = (data.room_id if data.room_id is not None else reservation.room_id)
        validate_reservation_dates(new_check_in, new_check_out)
        validate_room_availability(db, new_room_id, new_check_in, new_check_out, exclude_reservation_id=reservation_id)

    return repository.reservation_update(db, reservation, data)

def reservation_select_by_id(db: Session, reservation_id: int) -> Reservation:
    reservation = repository.get_reservation_by_id(db, reservation_id)

    if not reservation:
        raise ReservationNotFoundError("Reservation doesn't exist.")

    return reservation

def reservation_cancel(db: Session, reservation_id: int) -> Reservation:
    reservation = reservation_select_by_id(db, reservation_id)
    reservation.cancel()

    return repository.save(db, reservation)

def reservation_check_in(db: Session, reservation_id: int) -> Reservation:
    reservation = reservation_select_by_id(db, reservation_id)
    reservation.check_in()

    return repository.save(db, reservation)

def reservation_check_out(db: Session, reservation_id: int) -> Reservation:
    reservation = reservation_select_by_id(db, reservation_id)
    reservation.check_out()

    return repository.save(db, reservation)

def reservations_get_all(db: Session) -> list[Reservation]:
    return repository.get_all_reservations(db)

def reservations_search_by_guest(db: Session, guest_id: int) -> list[Reservation]:
    # checks if guest exists
    validate_guest_exists(db, guest_id)

    reservations = repository.get_reservation_by_guest(db, guest_id)

    if not reservations:
        raise ReservationNotFoundError("Guest has no reservations.")

    return reservations