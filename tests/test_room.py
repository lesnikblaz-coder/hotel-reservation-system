import pytest

from models import Room
from exceptions import NoChangesError

def test_activate_room():
    room = Room(
        room_number=1001,
        room_type="single",
        capacity=2,
        price_per_night=100,
        is_active=False
    )

    room.activate()

    assert room.is_active is True

def test_activate_already_active_room():
    room = Room(
        room_number=1001,
        room_type="single",
        capacity=2,
        price_per_night=100,
        is_active=True
    )

    with pytest.raises(NoChangesError):
        room.activate()

def test_deactivate_room():
    room = Room(
        room_number=1001,
        room_type="single",
        capacity=2,
        price_per_night=100,
        is_active=True
    )

    room.deactivate()

    assert room.is_active == False

def test_deactivate_already_inactive_room():
    room = Room(
        room_number=1001,
        room_type="single",
        capacity=2,
        price_per_night=100,
        is_active=False
    )

    with pytest.raises(NoChangesError):
        room.deactivate()

def test_total_price():
    room = Room(
        room_number=1001,
        room_type="single",
        capacity=2,
        price_per_night=100,
        is_active=True
    )

    nights = 7

    total_price = room.total_price(nights)
    correct_ans = room.price_per_night * nights

    assert total_price == correct_ans