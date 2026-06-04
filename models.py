from sqlalchemy import Integer, String, DECIMAL, Boolean, Date, ForeignKey, Sequence
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from decimal import Decimal

from database import Base
from constants import CANCELLABLE_STATUSES, CHECKIN_STATUSES, CHECKOUT_STATUSES
from exceptions import InvalidReservationStateError, InvalidCheckInDateError, CheckOutDatePassedError, NoChangesError

class Guest(Base):
    __tablename__ = "guests"

    guest_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    reservations: Mapped[list["Reservation"]] = relationship(back_populates="guest")

    def __repr__(self):
        return f'<Guest(guest_id={self.guest_id}, email={self.email})>'

    def full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'

class Room(Base):
    __tablename__ = "rooms"

    room_number_seq = Sequence("room_number_seq", start=1000)

    room_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    room_number: Mapped[int] = mapped_column(Integer, room_number_seq, server_default=room_number_seq.next_value(), nullable=False, unique=True)
    room_type: Mapped[str] = mapped_column(String, nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    price_per_night: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    reservations: Mapped[list["Reservation"]] = relationship(back_populates="room")

    def deactivate(self) -> None:
        if not self.is_active:
            raise NoChangesError("Room is already inactive.")

        self.is_active = False

    def activate(self) -> None:
        if self.is_active:
            raise NoChangesError("Room is already active.")

        self.is_active = True

    def total_price(self, nights: int) -> Decimal:
        return self.price_per_night * nights

class Reservation(Base):
    __tablename__ = "reservations"

    reservation_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    guest_id: Mapped[int] = mapped_column(Integer, ForeignKey("guests.guest_id"), nullable=False)
    room_id: Mapped[int] = mapped_column(Integer, ForeignKey("rooms.room_id"), nullable=False)
    check_in_date: Mapped[date] = mapped_column(Date, nullable=False)
    check_out_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)

    guest: Mapped["Guest"] = relationship(back_populates="reservations")
    room: Mapped["Room"] = relationship(back_populates="reservations")

    def duration_nights(self) -> int:
        return (self.check_out_date - self.check_in_date).days

    def cancel(self) -> None:
        if self.status not in CANCELLABLE_STATUSES:
            raise InvalidReservationStateError("Cannot cancel a reservation that isn't booked.")

        self.status = "cancelled"

    def check_in(self) -> None:
        if self.status not in CHECKIN_STATUSES:
            raise InvalidReservationStateError("Cannot check-in a reservation that isn't booked.")

        if self.check_in_date != date.today():
            raise InvalidCheckInDateError(f'Check-in unavailable. Check in date: {self.check_in_date}')

        self.status = "checked_in"

    def check_out(self) -> None:
        if self.status not in CHECKOUT_STATUSES:
            raise InvalidReservationStateError("Cannot check-out a reservation that wasn't checked-in yet.")

        if date.today() > self.check_out_date:
            raise CheckOutDatePassedError("Check-out date has passed.")

        self.status = "checked_out"