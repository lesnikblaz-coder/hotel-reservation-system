import enums
from decimal import Decimal

VALID_STATUSES = {
    enums.ReservationStatus.BOOKED.value,
    enums.ReservationStatus.CHECKED_IN.value,
    enums.ReservationStatus.CHECKED_OUT.value,
    enums.ReservationStatus.CANCELLED.value
}

CANCELLABLE_STATUSES = {enums.ReservationStatus.BOOKED.value}
CHECKIN_STATUSES = {enums.ReservationStatus.BOOKED.value}
CHECKOUT_STATUSES = {enums.ReservationStatus.CHECKED_IN.value}
NON_DELETABLE_STATUSES = {enums.ReservationStatus.BOOKED.value, enums.ReservationStatus.CHECKED_IN.value}

VALID_ROOM_TYPES = {
    enums.RoomType.SINGLE: {
        "capacity": 3,
        "price_per_night": Decimal("99.99")
    },
    enums.RoomType.DOUBLE: {
        "capacity": 5,
        "price_per_night": Decimal("179.99")
    },
    enums.RoomType.SUITE: {
        "capacity": 8,
        "price_per_night": Decimal("349.99")
    }
}

EMAIL_PATTERN = r"^[\w\.-]+@[\w\.-]+\.\w+$"

VALID_PHONE = "+0123456789"