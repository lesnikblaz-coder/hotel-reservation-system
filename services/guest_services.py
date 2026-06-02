import repository

from sqlalchemy.orm import Session

from models import Guest
from schemas import GuestUpdate
from constants import NON_DELETABLE_STATUSES
from exceptions import GuestNotFoundError, GuestHasActiveReservationsError, DuplicatePhoneError, DuplicateEmailError


def validate_email(db: Session, email: str) -> None:
    if repository.get_guest_by_email(db, email):
        raise DuplicateEmailError("Email already exists.")

def validate_phone(db: Session, phone: str) -> None:
    if repository.get_guest_by_phone(db, phone):
        raise DuplicatePhoneError("Phone number already exists.")

def guest_create(db: Session, first_name: str, last_name: str, email: str, phone: str) -> Guest:
    validate_email(db, email)
    validate_phone(db, phone)

    guest = Guest(first_name=first_name, last_name=last_name, email=email, phone=phone)

    return repository.guest_create(db, guest)

def guest_select_by_id(db: Session, guest_id: int) -> Guest:
    guest = repository.get_guest_by_id(db, guest_id)

    if guest is None:
        raise GuestNotFoundError("Guest does not exist.")

    return guest

def guest_delete(db: Session, guest_id: int) -> None:
    guest = guest_select_by_id(db, guest_id)
    reservations = repository.get_reservation_by_guest(db, guest_id)

    active_reservations = [r for r in reservations
                           if r.status in NON_DELETABLE_STATUSES]
    if active_reservations:
        raise GuestHasActiveReservationsError("Cannot delete a guest with an active reservation.")

    repository.guest_delete(db, guest)

def guest_update(db: Session, guest_id: int, data: GuestUpdate) -> Guest:
    guest = guest_select_by_id(db, guest_id)

    # validation step
    if data.email:
        validate_email(db, data.email)
    if data.phone:
        validate_phone(db, data.phone)

    return repository.guest_update(db, guest, data)

def guests_get_all(db: Session) -> list[Guest]:
    return repository.get_all_guests(db)