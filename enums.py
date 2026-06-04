from enum import Enum

class ReservationStatus(str, Enum):
    BOOKED = "booked"
    CHECKED_IN = "checked_in"
    CHECKED_OUT = "checked_out"
    CANCELLED = "cancelled"