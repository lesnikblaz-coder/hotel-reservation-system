import repository

from models import Guest
from constants import NON_DELETABLE_STATUSES
from exceptions import GuestNotFoundError, GuestHasActiveReservationsError, DuplicatePhoneError, DuplicateEmailError, InvalidFieldError, NoChangesError


def validate_email(email):
    if repository.get_guest_by_email(email):
        raise DuplicateEmailError("Email already exists.")

def validate_phone(phone: str):
    if repository.get_guest_by_phone(phone):
        raise DuplicatePhoneError("Phone number already exists.")

def validate_field(guest, field: str):
    try:
        return getattr(guest, field)
    except AttributeError:
        raise InvalidFieldError("Invalid field.")

def guest_create(first_name, last_name, email, phone):
    validate_email(email)
    validate_phone(phone)

    guest = Guest(first_name=first_name, last_name=last_name, email=email, phone=phone)
    new_guest_id = repository.guest_create(guest)
    guest.guest_id = new_guest_id
    return guest

def guest_select_by_id(guest_id):
    guest = repository.get_guest_by_id(guest_id)

    if guest is None:
        raise GuestNotFoundError("Guest does not exist.")

    return guest

def guest_delete(guest_id: int):
    guest = guest_select_by_id(guest_id)
    reservations = repository.get_reservation_by_guest(guest.guest_id)

    for r in reservations:
        if r.status in NON_DELETABLE_STATUSES:
            raise GuestHasActiveReservationsError("Cannot delete a guest with an active reservation.")

    repository.guest_delete(guest.guest_id)

def guest_update(guest_id, data):
    guest = guest_select_by_id(guest_id)

    if data.email:
        validate_email(data.email)
    if data.phone:
        validate_phone(data.phone)

    if (data.first_name == guest.first_name and
        data.last_name == guest.last_name and
        data.email == guest.email and
        data.phone == guest.phone
    ):
        raise NoChangesError("No changes detected.")

    repository.guest_update(guest_id, data)

    return repository.get_guest_by_id(guest_id)

def guests_get_all():
    guests = repository.get_all_guests()

    if not guests:
        raise GuestNotFoundError("No guests found.")

    return guests