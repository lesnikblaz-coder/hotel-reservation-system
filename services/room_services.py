import repository

from models import Room
from constants import VALID_ROOM_TYPES
from exceptions import InvalidRoomTypeError, RoomNotFoundError, ActiveReservationError, NoChangesError

def validate_room_type(room_type: str):
    room_data = VALID_ROOM_TYPES.get(room_type)

    if room_data is None:
        raise InvalidRoomTypeError(f"Invalid room type. Valid types: {', '.join(VALID_ROOM_TYPES.keys())}")

    return room_data

def room_create(room_type: str):
    room_data = validate_room_type(room_type)

    capacity = room_data["capacity"]
    price_per_night = room_data["price_per_night"]

    room = Room(room_type=room_type, capacity=capacity, price_per_night=price_per_night, is_active=True)

    new_room_keys = repository.room_create(room)
    room.room_id = new_room_keys["room_id"]
    room.room_number = new_room_keys["room_number"]
    print(f'DEBUG: room.room_id={room.room_id}')
    print(f'DEBUG: room.room_number={room.room_number}')

    return room

def room_select_by_id(room_id):
    room = repository.get_room_by_id(room_id)

    if room is None:
        raise RoomNotFoundError("Room not found.")

    return room

def room_delete(room_id):
    if repository.get_reservations_for_room(room_id):
        raise ActiveReservationError("Room has active reservations. Unable to delete.")

    repository.room_delete(room_id)

def room_deactivate(room):
    room.deactivate()
    repository.room_update(room.room_id, room)

def room_activate(room):
    room.activate()
    repository.room_update(room.room_id, room)

def rooms_get_all():
    rooms = repository.get_all_rooms()

    if not rooms:
        raise RoomNotFoundError("No rooms found.")

    return rooms

def rooms_get_available():
    available_rooms = repository.get_available_rooms()

    if not available_rooms:
        raise RoomNotFoundError("No available rooms.")

    return available_rooms

def room_update(room_id, data):
    room = room_select_by_id(room_id)

    if data.room_type:
        validate_room_type(data.room_type)

    if (data.room_type == room.room_type and
        data.capacity == room.capacity and
        data.price_per_night == room.price_per_night and
        data.is_active == room.is_active
    ):
        raise NoChangesError("New value same as old value.")

    repository.room_update(room_id, data)

    return repository.get_room_by_id(room_id)

def validate_field(room, field: str):
    try:
        return getattr(room, field)
    except AttributeError:
        raise ValueError("Invalid field.")

def get_first_room_each_type():
    rooms = repository.get_first_room_per_type()

    if not rooms:
        raise RoomNotFoundError("No rooms found.")

    return rooms