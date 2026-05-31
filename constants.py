VALID_STATUSES = {
    "booked",
    "checked_in",
    "checked_out",
    "cancelled"
}

CANCELLABLE_STATUSES = {"booked"}
CHECKIN_STATUSES = {"booked"}
CHECKOUT_STATUSES = {"checked_in"}
NON_DELETABLE_STATUSES = {"booked", "checked_in"}

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