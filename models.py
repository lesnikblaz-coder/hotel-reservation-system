from datetime import date
from pydantic import BaseModel

from constants import CANCELLABLE_STATUSES, CHECKIN_STATUSES, CHECKOUT_STATUSES
from exceptions import InvalidReservationStateError, InvalidCheckInDateError, CheckOutDatePassedError, NoChangesError

class Guest(BaseModel):
    guest_id: int | None = None
    first_name: str
    last_name: str
    email: str
    phone: str

    def __str__(self):
        return(
            f'Guest ID: {self.guest_id}, '
            f'first name: {self.first_name}, '
            f'last name: {self.last_name}, '
            f'email: {self.email}, '
            f'phone: {self.phone}'
        )

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

class Room(BaseModel):
    room_id: int | None = None
    room_number: int | None = None
    room_type: str
    capacity: int
    price_per_night: float
    is_active: bool

    def __str__(self):
        return (
            f'Room ID: {self.room_id}, '
            f'room number: {self.room_number}, '
            f'room type: {self.room_type}, '
            f'capacity: {self.capacity}, '
            f'price per night: {self.price_per_night}, '
            f'is active: {self.is_active}'
        )

    def deactivate(self):
        if not self.is_active:
            raise NoChangesError("Room is already inactive.")

        self.is_active = False

    def activate(self):
        if self.is_active:
            raise NoChangesError("Room is already active.")

        self.is_active = True

    def total_price(self, nights: int):
        return self.price_per_night * nights

class Reservation(BaseModel):
    reservation_id: int | None = None
    guest_id: int
    room_id: int
    check_in_date: date
    check_out_date: date
    status: str

    def __str__(self):
        return (
            f'Reservation ID: {self.reservation_id}, '
            f'Guest ID: {self.guest_id}, '
            f'Room ID: {self.room_id}, '
            f'check in date: {self.check_in_date}, '
            f'check out date: {self.check_out_date}, '
            f'status: {self.status}'
        )

    def duration_nights(self):
        ci = self.check_in_date
        co = self.check_out_date

        return (co - ci).days

    def cancel(self):
        if self.status not in CANCELLABLE_STATUSES:
            raise InvalidReservationStateError("Cannot cancel a reservation that isn't booked.")

        self.status = "cancelled"

    def check_in(self):
        if self.status not in CHECKIN_STATUSES:
            raise InvalidReservationStateError("Cannot check-in a reservation that isn't booked.")

        if self.check_in_date != date.today():
            raise InvalidCheckInDateError(f'Check-in unavailable. Check in date: {self.check_in_date}')

        self.status = "checked_in"

    def check_out(self):
        if self.status not in CHECKOUT_STATUSES:
            raise InvalidReservationStateError("Cannot check-out a reservation that wasn't checked-in yet.")

        if date.today() > self.check_out_date:
            raise CheckOutDatePassedError("Check-out date has passed.")

        self.status = "checked_out"