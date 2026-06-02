from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import date

from models import Guest, Room, Reservation
from schemas import GuestUpdate, RoomUpdate

#GUESTS
def get_all_guests(db: Session) -> list[Guest]:
    return list(db.scalars(select(Guest)).all())

def get_guest_by_id(db: Session, guest_id: int) -> Guest | None:
    return db.scalars(select(Guest).where(Guest.guest_id == guest_id)).first()

def get_guest_by_email(db: Session, email: str) -> Guest | None:
    return db.scalars(select(Guest).where(Guest.email == email)).first()

def get_guest_by_phone(db: Session, phone: str) -> Guest | None:
    return db.scalars(select(Guest).where(Guest.phone == phone)).first()

def guest_create(db: Session, guest: Guest) -> Guest:
    db.add(guest)
    db.commit()
    db.refresh(guest)

    return guest

def guest_delete(db: Session, guest: Guest) -> Guest:
    db.delete(guest)
    db.commit()

    return guest

def guest_update(db: Session, guest: Guest, data: GuestUpdate) -> Guest:
    if data.first_name is not None:
        guest.first_name = data.first_name

    if data.last_name is not None:
        guest.last_name = data.last_name

    if data.email is not None:
        guest.email = data.email

    if data.phone is not None:
        guest.phone = data.phone

    db.commit()
    db.refresh(guest)

    return guest

#ROOMS
def get_all_rooms(db: Session) -> list[Room]:
    return list(db.scalars(select(Room)).all())

def get_room_by_id(db: Session, room_id: int) -> Room | None:
    return db.scalars(select(Room).where(Room.room_id == room_id)).first()

def room_create(db: Session, room: Room) -> Room:
    db.add(room)
    db.commit()
    db.refresh(room)

    return room

def room_delete(db: Session, room: Room) -> Room:
    db.delete(room)
    db.commit()

    return room

def room_update(db: Session, room: Room, data: RoomUpdate) -> Room:
    if data.room_type is not None:
        room.room_type = data.room_type

    if data.capacity is not None:
        room.capacity = data.capacity

    if data.price_per_night is not None:
        room.price_per_night = data.price_per_night

    if data.is_active is not None:
        room.is_active = data.is_active

    db.commit()
    db.refresh(room)

    return room

def get_available_rooms(db: Session) -> list[Room]:
    return list(db.scalars(select(Room).where(Room.is_active)).all())

def room_save(db: Session, room: Room) -> Room:
    db.commit()
    db.refresh(room)

    return room

#RESERVATIONS
def get_all_reservations(db: Session) -> list[Reservation]:
    return list(db.scalars(select(Reservation)).all())

def get_reservation_by_guest(db: Session, guest_id: int) -> list[Reservation]:
    return list(db.scalars(select(Reservation).where(Reservation.guest_id == guest_id)).all())

def reservation_create(db: Session, reservation: Reservation) -> Reservation:
    db.add(reservation)
    db.commit()
    db.refresh(reservation)

    return reservation

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
    return list(db.scalars(select(Reservation).where(Reservation.room_id == room_id)).all())

def reservation_save(db: Session, reservation: Reservation) -> Reservation:
    db.commit()
    db.refresh(reservation)

    return reservation