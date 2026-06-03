from sqlalchemy.orm import Session

import repository

from models import Room
from schemas import RoomUpdate
from constants import VALID_ROOM_TYPES, NON_DELETABLE_STATUSES
from exceptions import InvalidRoomTypeError, RoomNotFoundError, ActiveReservationError

def validate_room_type(room_type: str) -> dict[str, int | float]:
    room_data = VALID_ROOM_TYPES.get(room_type)

    if room_data is None:
        raise InvalidRoomTypeError(f"Invalid room type. Valid types: {', '.join(VALID_ROOM_TYPES.keys())}")

    return room_data

def room_create(db: Session, room_type: str) -> Room:
    # validate room type existence
    room_data = validate_room_type(room_type)

    capacity = room_data["capacity"]
    price_per_night = room_data["price_per_night"]

    room = Room(room_type=room_type, capacity=capacity, price_per_night=price_per_night, is_active=True)

    return repository.room_create(db, room)

def room_select_by_id(db: Session, room_id: int) -> Room:
    room = repository.get_room_by_id(db, room_id)

    if room is None:
        raise RoomNotFoundError("Room not found.")

    return room

def room_delete(db: Session, room_id: int) -> None:
    reservations = repository.get_reservations_for_room(db, room_id)

    # only reservations with status "checked_out" or "cancelled" can be deleted.
    active_reservations = [r for r in reservations
                           if r.status in NON_DELETABLE_STATUSES]

    if active_reservations:
        raise ActiveReservationError("Room has active reservations. Unable to delete.")

    room = room_select_by_id(db, room_id)

    repository.room_delete(db, room)

def room_deactivate(db: Session, room_id: int) -> Room:
    room = room_select_by_id(db, room_id)
    room.deactivate()
    return repository.save(db, room)

def room_activate(db: Session, room_id: int) -> Room:
    room = room_select_by_id(db, room_id)
    room.activate()
    return repository.save(db, room)

def rooms_get_all(db: Session) -> list[Room]:
    return repository.get_all_rooms(db)

def rooms_get_available(db: Session) -> list[Room]:
    available_rooms = repository.get_available_rooms(db)

    if not available_rooms:
        raise RoomNotFoundError("No available rooms.")

    return available_rooms

def room_update(db: Session, room_id: int, data: RoomUpdate) -> Room:
    room = room_select_by_id(db, room_id)

    if data.room_type:
        validate_room_type(data.room_type)

    return repository.room_update(db, room, data)