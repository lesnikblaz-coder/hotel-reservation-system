from fastapi.responses import JSONResponse

import exceptions


def register_exception_handlers(app):
    @app.exception_handler(exceptions.GuestNotFoundError)
    def guest_not_found(_, exc: exceptions.GuestNotFoundError):
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(exceptions.DuplicateEmailError)
    def duplicate_email(_, exc: exceptions.DuplicateEmailError):
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    @app.exception_handler(exceptions.DuplicatePhoneError)
    def duplicate_phone(_, exc: exceptions.DuplicatePhoneError):
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    @app.exception_handler(exceptions.GuestHasActiveReservationsError)
    def guest_has_reservations(_, exc: exceptions.GuestHasActiveReservationsError):
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    @app.exception_handler(exceptions.NoChangesError)
    def no_changes(_, exc: exceptions.NoChangesError):
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    @app.exception_handler(exceptions.InvalidRoomTypeError)
    def invalid_room_type(_, exc: exceptions.InvalidRoomTypeError):
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    @app.exception_handler(exceptions.RoomNotFoundError)
    def room_not_found(_, exc: exceptions.RoomNotFoundError):
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(exceptions.ActiveReservationError)
    def active_reservation(_, exc: exceptions.ActiveReservationError):
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    @app.exception_handler(exceptions.ReservationNotFoundError)
    def reservation_not_found(_, exc: exceptions.ReservationNotFoundError):
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(exceptions.InvalidDateFormatError)
    def invalid_date_format(_, exc: exceptions.InvalidDateFormatError):
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    @app.exception_handler(exceptions.ConflictingDateError)
    def conflicting_date(_, exc: exceptions.ConflictingDateError):
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    @app.exception_handler(exceptions.InvalidReservationStateError)
    def invalid_reservation_state(_, exc: exceptions.InvalidReservationStateError):
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    @app.exception_handler(exceptions.InvalidCheckInDateError)
    def invalid_check_in_date(_, exc: exceptions.InvalidCheckInDateError):
        return JSONResponse(status_code=422, content={"detail": str(exc)})

    @app.exception_handler(exceptions.CheckOutDatePassedError)
    def check_out_date_passed(_, exc: exceptions.CheckOutDatePassedError):
        return JSONResponse(status_code=422, content={"detail": str(exc)})