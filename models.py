from sqlalchemy import Integer, String, DECIMAL, Boolean, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from decimal import Decimal

from database import Base
from exceptions import InvalidReservationStateError, InvalidCheckInDateError, CheckOutDatePassedError, NoChangesError

import enums

class Guest(Base):
    __tablename__ = "guests"

    guest_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    reservations: Mapped[list["Reservation"]] = relationship(back_populates="guest")

    def __repr__(self):
        return (f'<Guest(guest_id={self.guest_id}, '
                f'first_name={self.first_name}, '
                f'last_name={self.last_name}, '
                f'email={self.email}, '
                f'phone={self.phone}'
                f')>')

    def full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'

class Room(Base):
    __tablename__ = "rooms"

    room_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    room_number: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)
    room_type: Mapped[str] = mapped_column(String, nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    price_per_night: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    reservations: Mapped[list["Reservation"]] = relationship(back_populates="room")

    def __repr__(self):
        return (f'<Room(room_id={self.room_id}, '
                f'room_number={self.room_number}, '
                f'room_type={self.room_type}, '
                f'capacity={self.capacity}, '
                f'price_per_night={self.price_per_night}, '
                f'is_active={self.is_active}'
                f')>')

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
    status: Mapped[enums.ReservationStatus] = mapped_column(String, nullable=False)
    total_price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)

    guest: Mapped["Guest"] = relationship(back_populates="reservations")
    room: Mapped["Room"] = relationship(back_populates="reservations")

    def __repr__(self):
        return (f'<Reservation(reservation_id={self.reservation_id}, '
                f'guest_id={self.guest_id}, '
                f'room_id={self.room_id}, '
                f'check_in_date={self.check_in_date}, '
                f'check_out_date={self.check_out_date}, '
                f'status={self.status}, '
                f'total_price={self.total_price}'
                f')>')

    def duration_nights(self) -> int:
        return (self.check_out_date - self.check_in_date).days

    def cancel(self) -> None:
        if self.status != enums.ReservationStatus.BOOKED:
            raise InvalidReservationStateError("Only booked reservations can be cancelled.")

        self.status = enums.ReservationStatus.CANCELLED

    def check_in(self) -> None:
        if self.status != enums.ReservationStatus.BOOKED:
            raise InvalidReservationStateError("Only booked reservations can be checked in.")

        if self.check_in_date != date.today():
            raise InvalidCheckInDateError(f'Check-in allowed only on {self.check_in_date}')

        self.status = enums.ReservationStatus.CHECKED_IN

    def check_out(self) -> None:
        if self.status != enums.ReservationStatus.CHECKED_IN:
            raise InvalidReservationStateError("Only checked-in reservations can be checked out.")

        if date.today() < self.check_in_date:
            raise CheckOutDatePassedError("Cannot check out before check-in date.")

        self.status = enums.ReservationStatus.CHECKED_OUT

class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    role: Mapped[str] = mapped_column(String, nullable=False, default=enums.UserRole.GUEST.value)