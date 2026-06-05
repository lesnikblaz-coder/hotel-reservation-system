import enums

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