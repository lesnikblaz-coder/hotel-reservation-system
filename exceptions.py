class GuestNotFoundError(Exception):
    pass

class GuestHasActiveReservationsError(Exception):
    pass

class DuplicateEmailError(Exception):
    pass

class DuplicatePhoneError(Exception):
    pass

class NoChangesError(Exception):
    pass

class InvalidRoomTypeError(Exception):
    pass

class RoomNotFoundError(Exception):
    pass

class ActiveReservationError(Exception):
    pass
class ReservationNotFoundError(Exception):
    pass

class InvalidDateFormatError(Exception):
    pass

class ConflictingDateError(Exception):
    pass

class InvalidReservationStateError(Exception):
    pass

class InvalidCheckInDateError(Exception):
    pass

class CheckOutDatePassedError(Exception):
    pass

class InvalidPhoneNumberError(Exception):
    pass

class ConflictingRoomNumberError(Exception):
    pass

class InvalidRoomNumberError(Exception):
    pass

class InvalidCredentialsError(Exception):
    pass

class InvalidTokenError(Exception):
    pass

class UserNotFoundError(Exception):
    pass

class InsufficientPermissions(Exception):
    pass