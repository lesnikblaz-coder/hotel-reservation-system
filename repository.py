from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import date

from models import Guest, Room, Reservation
from schemas import GuestUpdate, RoomUpdate

# centralized database saving
def save(db: Session, obj):
    db.commit()
    db.refresh(obj)

    return obj

#GUESTS
def get_all_guests(db: Session) -> list[Guest]:
    return list(db.scalars(select(Guest).order_by(Guest.guest_id)).all())

def get_guest_by_id(db: Session, guest_id: int) -> Guest | None:
    return db.scalars(select(Guest).where(Guest.guest_id == guest_id)).first()

def get_guest_by_email(db: Session, email: str) -> Guest | None:
    return db.scalars(select(Guest).where(Guest.email == email)).first()

def get_guest_by_phone(db: Session, phone: str) -> Guest | None:
    return db.scalars(select(Guest).where(Guest.phone == phone)).first()

def guest_create(db: Session, guest: Guest) -> Guest:
    db.add(guest)
    return save(db, guest)

def guest_delete(db: Session, guest: Guest) -> Guest:
    db.delete(guest)
    return save(db, guest)

def guest_update(db: Session, guest: Guest, data: GuestUpdate) -> Guest:
    if data.first_name is not None:
        guest.first_name = data.first_name

    if data.last_name is not None:
        guest.last_name = data.last_name

    if data.email is not None:
        guest.email = data.email

    if data.phone is not None:
        guest.phone = data.phone

    return save(db, guest)

#ROOMS
def get_all_rooms(db: Session) -> list[Room]:
    return list(db.scalars(select(Room).order_by(Room.room_id)).all())

def get_room_by_id(db: Session, room_id: int) -> Room | None:
    return db.scalars(select(Room).where(Room.room_id == room_id)).first()

def room_create(db: Session, room: Room) -> Room:
    db.add(room)
    return save(db, room)

def room_delete(db: Session, room: Room) -> Room:
    db.delete(room)
    return save(db, room)

def room_update(db: Session, room: Room, data: RoomUpdate) -> Room:
    if data.room_type is not None:
        room.room_type = data.room_type

    if data.capacity is not None:
        room.capacity = data.capacity

    if data.price_per_night is not None:
        room.price_per_night = data.price_per_night

    if data.is_active is not None:
        room.is_active = data.is_active

    return save(db, room)

def get_available_rooms(db: Session) -> list[Room]:
    return list(db.scalars(select(Room).where(Room.is_active).order_by(Room.room_id)).all())

#RESERVATIONS
def get_all_reservations(db: Session) -> list[Reservation]:
    return list(db.scalars(select(Reservation).order_by(Reservation.reservation_id)).all())

def get_reservation_by_guest(db: Session, guest_id: int) -> list[Reservation]:
    return list(db.scalars(select(Reservation).where(Reservation.guest_id == guest_id).order_by(Reservation.reservation_id)).all())

def reservation_create(db: Session, reservation: Reservation) -> Reservation:
    db.add(reservation)
    return save(db, reservation)

def get_conflicting_reservations(db:Session, room_id: int, new_check_in: date, new_check_out: date) -> Reservation | None:
    return db.scalars(select(Reservation).where(
        Reservation.room_id == room_id,
        Reservation.status.notin_(["checked_out", "cancelled"]),
        Reservation.check_in_date < new_check_out,
        Reservation.check_out_date > new_check_in
    )).first()

def get_reservation_by_id(db: Session, reservation_id: int) -> Reservation | None:
    return db.scalars(select(Reservation).where(Reservation.reservation_id == reservation_id)).first()

def get_reservations_for_room(db: Session, room_id: int) -> list[Reservation]:
    return list(db.scalars(select(Reservation).where(Reservation.room_id == room_id).order_by(Reservation.reservation_id)).all())