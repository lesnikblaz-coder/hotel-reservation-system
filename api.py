from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated

from database import get_db
from services import guest_services, room_services, reservation_services, report_services, auth_services
from exception_handlers import register_exception_handlers

import schemas, models, auth

app = FastAPI()
register_exception_handlers(app)

@app.get("/", include_in_schema=False)
def root() -> dict[str, str]:
    return {"status": "ok"}

db_session = Annotated[Session, Depends(get_db)]

# --- guests ---
@app.post("/guests", status_code=201 , response_model=schemas.GuestResponse)
def guest_create(request: schemas.GuestCreate, db: db_session) -> models.Guest:
    return guest_services.guest_create(
        db,
        request.first_name,
        request.last_name,
        request.email,
        request.phone
    )

@app.get("/guests", response_model=list[schemas.GuestResponse], dependencies=[Depends(auth.get_current_user)])
def guests_get(db: db_session) -> list[models.Guest]:
    return guest_services.guests_get_all(db)

@app.get("/guests/{guest_id}", response_model=schemas.GuestResponse)
def guest_get(guest_id: int, db: db_session) -> models.Guest:
    return guest_services.guest_select_by_id(db, guest_id)

@app.put("/guests/{guest_id}", response_model=schemas.GuestResponse)
def guest_update(guest_id: int, request: schemas.GuestUpdate, db: db_session) -> models.Guest | None:
    return guest_services.guest_update(db, guest_id, request)

@app.delete("/guests/{guest_id}", status_code=204)
def guest_delete(guest_id: int, db: db_session) -> None:
    guest_services.guest_delete(db, guest_id)


# --- rooms ---
@app.post("/rooms", status_code=201, response_model=schemas.RoomResponse)
def room_create(request: schemas.RoomCreate, db: db_session) -> models.Room:
    return room_services.room_create(db, request.room_type, request.room_number)

@app.get("/rooms", response_model=list[schemas.RoomResponse])
def rooms_get(db: db_session) -> list[models.Room]:
    return room_services.rooms_get_all(db)

@app.post("/rooms/availability", response_model=list[schemas.RoomResponse])
def search_available_rooms(search: schemas.RoomAvailabilitySearch, db: db_session) -> list[models.Room]:
    return room_services.rooms_get_available(db, search)

@app.get("/rooms/{room_id}", response_model=schemas.RoomResponse)
def room_get(room_id: int, db: db_session) -> models.Room:
    return room_services.room_select_by_id(db, room_id)

@app.put("/rooms/{room_id}", response_model=schemas.RoomResponse)
def room_update(room_id: int, request: schemas.RoomUpdate, db: db_session) -> models.Room | None:
    return room_services.room_update(db, room_id, request)

@app.delete("/rooms/{room_id}", status_code=204)
def room_delete(room_id: int, db: db_session) -> None:
    room_services.room_delete(db, room_id)

@app.post("/rooms/{room_id}/activate", response_model=schemas.RoomResponse)
def room_activate(room_id: int, db: db_session) -> models.Room:
    return room_services.room_activate(db, room_id)

@app.post("/rooms/{room_id}/deactivate", response_model=schemas.RoomResponse)
def room_deactivate(room_id: int, db: db_session) -> models.Room:
    return room_services.room_deactivate(db, room_id)


# --- reservations ---
@app.post("/reservations", status_code=201, response_model=schemas.ReservationResponse)
def reservation_create(request: schemas.ReservationCreate, db: db_session) -> models.Reservation:
    return reservation_services.reservation_create(
        db,
        request.guest_id,
        request.room_id,
        request.check_in_date,
        request.check_out_date
    )

@app.get("/reservations", response_model=list[schemas.ReservationResponse])
def reservations_get(db: db_session) -> list[models.Reservation]:
    return reservation_services.reservations_get_all(db)

@app.get("/reservations/{reservation_id}", response_model=schemas.ReservationResponse)
def reservation_get(reservation_id: int, db: db_session) -> models.Reservation:
    return reservation_services.reservation_select_by_id(db, reservation_id)

@app.put("/reservations/{reservation_id}", response_model=schemas.ReservationResponse)
def reservation_update(reservation_id: int, request: schemas.ReservationUpdate, db: db_session) -> models.Reservation:
    return reservation_services.reservation_update(db, reservation_id, request)

@app.post("/reservations/{reservation_id}/cancel", response_model=schemas.ReservationResponse)
def reservation_cancel(reservation_id: int, db: db_session) -> models.Reservation:
    return reservation_services.reservation_cancel(db, reservation_id)

@app.post("/reservations/{reservation_id}/check-in", response_model=schemas.ReservationResponse)
def reservation_check_in(reservation_id: int, db: db_session) -> models.Reservation:
    return reservation_services.reservation_check_in(db, reservation_id)

@app.post("/reservations/{reservation_id}/check-out", response_model=schemas.ReservationResponse)
def reservation_check_out(reservation_id: int, db: db_session) -> models.Reservation:
    return reservation_services.reservation_check_out(db, reservation_id)

# --- REPORTS ---
# --- revenue ---
@app.post("/reports/revenue", response_model=schemas.RevenueReportResponse)
def revenue_report(request: schemas.RevenueReportRequest, db: db_session) -> schemas.RevenueReportResponse:
    revenue = report_services.revenue_report(db, request)
    return schemas.RevenueReportResponse(revenue=revenue)

@app.get("/reports/revenue/monthly", response_model=list[schemas.MonthlyRevenueReportResponse])
def revenue_report_monthly(db: db_session) -> list[schemas.MonthlyRevenueReportResponse]:
    return report_services.revenue_report_monthly(db)

@app.get("/reports/revenue/yearly", response_model=list[schemas.YearlyRevenueReportResponse])
def revenue_report_yearly(db: db_session) -> list[schemas.YearlyRevenueReportResponse]:
    return report_services.revenue_report_yearly(db)

@app.get("/reports/occupancy/today", response_model=schemas.OccupancyReportResponse)
def occupancy_report(db: db_session) -> schemas.OccupancyReportResponse:
    return report_services.occupancy_report(db)

@app.post("/reports/occupancy/monthly", response_model=schemas.MonthlyOccupancyReportResponse)
def occupancy_report_monthly(request: schemas.OccupancyReportRequest, db: db_session) -> schemas.MonthlyOccupancyReportResponse:
    return report_services.occupancy_report_monthly(db, request)

# --- JWT AUTHENTICATION ---
@app.post("/auth/register", status_code=201)
def register(request: schemas.UserRegister, db: db_session):
    return auth_services.register(db, request.email, request.password)

@app.post("/auth/login", response_model=schemas.TokenResponse)
def login(request: schemas.UserLogin, db: db_session) -> schemas.TokenResponse:
    return auth_services.login(db, request.email, request.password)

@app.post("/auth/token", response_model=schemas.TokenResponse)
def token(db: db_session, form_data: OAuth2PasswordRequestForm = Depends()) -> schemas.TokenResponse:
    return auth_services.login(db, form_data.username, form_data.password)