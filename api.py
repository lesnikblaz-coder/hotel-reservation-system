from contextlib import asynccontextmanager
from fastapi import FastAPI

from database import guest_db, rooms_db, reservations_db
from services import guest_services, room_services, reservation_services
from exception_handlers import register_exception_handlers

import schemas

@asynccontextmanager
async def lifespan(_: FastAPI):
    # startup code
    guest_db.create_guests_table()
    rooms_db.create_rooms_table()
    reservations_db.create_reservations_table()

    yield

app = FastAPI(lifespan=lifespan)
register_exception_handlers(app)

@app.get("/", include_in_schema=False)
def root() -> dict[str, str]:
    return {"status": "ok"}

# --- guests ---
@app.post("/guests", status_code=201 , response_model=schemas.GuestResponse)
def guest_create(request: schemas.GuestCreate) -> schemas.GuestResponse:
    return guest_services.guest_create(
        request.first_name,
        request.last_name,
        request.email,
        request.phone
    )

@app.get("/guests", response_model=list[schemas.GuestResponse])
def guests_get() -> list[schemas.GuestResponse]:
    return guest_services.guests_get_all()

@app.get("/guests/{guest_id}", response_model=schemas.GuestResponse)
def guest_get(guest_id: int) -> schemas.GuestResponse:
    return guest_services.guest_select_by_id(guest_id)

@app.put("/guests/{guest_id}", response_model=schemas.GuestResponse)
def guest_update(guest_id: int, request: schemas.GuestUpdate) -> schemas.GuestResponse | None:
    return guest_services.guest_update(guest_id, request)

@app.delete("/guests/{guest_id}", status_code=204)
def guest_delete(guest_id: int) -> None:
    guest_services.guest_delete(guest_id)


# --- rooms ---
@app.post("/rooms", status_code=201, response_model=schemas.RoomResponse)
def room_create(request: schemas.RoomCreate) -> schemas.RoomResponse:
    return room_services.room_create(
        request.room_type
    )

@app.get("/rooms", response_model=list[schemas.RoomResponse])
def rooms_get() -> list[schemas.RoomResponse]:
    return room_services.rooms_get_all()

@app.get("/rooms/available", response_model=list[schemas.RoomResponse])
def rooms_get_available() -> list[schemas.RoomResponse]:
    return room_services.rooms_get_available()

@app.get("/rooms/{room_id}", response_model=schemas.RoomResponse)
def room_get(room_id: int) -> schemas.RoomResponse:
    return room_services.room_select_by_id(room_id)

@app.put("/rooms/{room_id}", response_model=schemas.RoomResponse)
def room_update(room_id: int, request: schemas.RoomUpdate) -> schemas.RoomResponse | None:
    return room_services.room_update(room_id, request)

@app.delete("/rooms/{room_id}", status_code=204)
def room_delete(room_id: int) -> None:
    room_services.room_delete(room_id)


# --- reservations ---
@app.post("/reservations", status_code=201, response_model=schemas.ReservationResponse)
def reservation_create(request: schemas.ReservationCreate) -> schemas.ReservationResponse:
    return reservation_services.reservation_create(
        request.guest_id,
        request.room_id,
        request.check_in_date,
        request.check_out_date
    )

@app.get("/reservations", response_model=list[schemas.ReservationResponse])
def reservations_get() -> list[schemas.ReservationResponse]:
    return reservation_services.reservations_get_all()

@app.get("/reservations/{reservation_id}", response_model=schemas.ReservationResponse)
def reservation_get(reservation_id: int) -> schemas.ReservationResponse:
    return reservation_services.reservation_select_by_id(reservation_id)

@app.put("/reservations/{reservation_id}/cancel", response_model=schemas.ReservationResponse)
def reservation_cancel(reservation_id: int) -> schemas.ReservationResponse:
    return reservation_services.reservation_cancel(reservation_id)

@app.put("/reservations/{reservation_id}/check-in", response_model=schemas.ReservationResponse)
def reservation_check_in(reservation_id: int) -> schemas.ReservationResponse:
    return reservation_services.reservation_check_in(reservation_id)

@app.put("/reservations/{reservation_id}/check-out", response_model=schemas.ReservationResponse)
def reservation_check_out(reservation_id: int) -> schemas.ReservationResponse:
    return reservation_services.reservation_check_out(reservation_id)