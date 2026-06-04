import enums

VALID_STATUSES = {
    enums.ReservationStatus.BOOKED,
    enums.ReservationStatus.CHECKED_IN,
    enums.ReservationStatus.CHECKED_OUT,
    enums.ReservationStatus.CANCELLED
}

CANCELLABLE_STATUSES = {enums.ReservationStatus.BOOKED}
CHECKIN_STATUSES = {enums.ReservationStatus.BOOKED}
CHECKOUT_STATUSES = {enums.ReservationStatus.CHECKED_IN}
NON_DELETABLE_STATUSES = {enums.ReservationStatus.BOOKED, enums.ReservationStatus.CHECKED_IN}

VALID_ROOM_TYPES = {
    "single": {
        "capacity": 3,
        "price_per_night": 99.99
    },
    "double": {
        "capacity": 5,
        "price_per_night": 179.99
    },
    "suite": {
        "capacity": 8,
        "price_per_night": 349.99
    }
}

EMAIL_PATTERN = r"^[\w\.-]+@[\w\.-]+\.\w+$"

VALID_PHONE = "+0123456789"