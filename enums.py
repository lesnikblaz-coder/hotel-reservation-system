from enum import StrEnum

class ReservationStatus(StrEnum):
    BOOKED = "booked"
    CHECKED_IN = "checked_in"
    CHECKED_OUT = "checked_out"
    CANCELLED = "cancelled"

class UserRole(StrEnum):
    GUEST = "guest"
    STAFF = "staff"
    ADMIN = "admin"