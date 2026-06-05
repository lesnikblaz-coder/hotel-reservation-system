from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from decimal import Decimal

from database import get_db
from services import guest_services, room_services, reservation_services, report_services
from exception_handlers import register_exception_handlers

import schemas, models

app = FastAPI()
register_exception_handlers(app)

@app.get("/", include_in_schema=False)
def root() -> dict[str, str]:
    return {"status": "ok"}

# --- guests ---
@app.post("/guests", status_code=201 , response_model=schemas.GuestResponse)
def guest_create(request: schemas.GuestCreate, db: Session = Depends(get_db)) -> models.Guest:
    return guest_services.guest_create(
        db,
        request.first_name,
        request.last_name,
        request.email,
        request.phone
    )

@app.get("/guests", response_model=list[schemas.GuestResponse])
def guests_get(db: Session = Depends(get_db)) -> list[models.Guest]:
    return guest_services.guests_get_all(db)

@app.get("/guests/{guest_id}", response_model=schemas.GuestResponse)
def guest_get(guest_id: int, db: Session = Depends(get_db)) -> models.Guest:
    return guest_services.guest_select_by_id(db, guest_id)

@app.put("/guests/{guest_id}", response_model=schemas.GuestResponse)
def guest_update(guest_id: int, request: schemas.GuestUpdate, db: Session = Depends(get_db)) -> models.Guest | None:
    return guest_services.guest_update(db, guest_id, request)

@app.delete("/guests/{guest_id}", status_code=204)
def guest_delete(guest_id: int, db: Session = Depends(get_db)) -> None:
    guest_services.guest_delete(db, guest_id)


# --- rooms ---
@app.post("/rooms", status_code=201, response_model=schemas.RoomResponse)
def room_create(request: schemas.RoomCreate, db: Session = Depends(get_db)) -> models.Room:
    return room_services.room_create(db, request.room_type, request.room_number)

@app.get("/rooms", response_model=list[schemas.RoomResponse])
def rooms_get(db: Session = Depends(get_db)) -> list[models.Room]:
    return room_services.rooms_get_all(db)

@app.post("/rooms/availability", response_model=list[schemas.RoomResponse])
def search_available_rooms(search: schemas.RoomAvailabilitySearch, db: Session = Depends(get_db)) -> list[models.Room]:
    return room_services.rooms_get_available(db, search)

@app.get("/rooms/{room_id}", response_model=schemas.RoomResponse)
def room_get(room_id: int, db: Session = Depends(get_db)) -> models.Room:
    return room_services.room_select_by_id(db, room_id)

@app.put("/rooms/{room_id}", response_model=schemas.RoomResponse)
def room_update(room_id: int, request: schemas.RoomUpdate, db: Session = Depends(get_db)) -> models.Room | None:
    return room_services.room_update(db, room_id, request)

@app.delete("/rooms/{room_id}", status_code=204)
def room_delete(room_id: int, db: Session = Depends(get_db)) -> None:
    room_services.room_delete(db, room_id)

@app.post("/rooms/{room_id}/activate", response_model=schemas.RoomResponse)
def room_activate(room_id: int, db: Session = Depends(get_db)) -> models.Room:
    return room_services.room_activate(db, room_id)

@app.post("/rooms/{room_id}/deactivate", response_model=schemas.RoomResponse)
def room_deactivate(room_id: int, db: Session = Depends(get_db)) -> models.Room:
    return room_services.room_deactivate(db, room_id)


# --- reservations ---
@app.post("/reservations", status_code=201, response_model=schemas.ReservationResponse)
def reservation_create(request: schemas.ReservationCreate, db: Session = Depends(get_db)) -> models.Reservation:
    return reservation_services.reservation_create(
        db,
        request.guest_id,
        request.room_id,
        request.check_in_date,
        request.check_out_date
    )

@app.get("/reservations", response_model=list[schemas.ReservationResponse])
def reservations_get(db: Session = Depends(get_db)) -> list[models.Reservation]:
    return reservation_services.reservations_get_all(db)

@app.get("/reservations/{reservation_id}", response_model=schemas.ReservationResponse)
def reservation_get(reservation_id: int, db: Session = Depends(get_db)) -> models.Reservation:
    return reservation_services.reservation_select_by_id(db, reservation_id)

@app.put("/reservations/{reservation_id}", response_model=schemas.ReservationResponse)
def reservation_update(reservation_id: int, request: schemas.ReservationUpdate, db: Session = Depends(get_db)) -> models.Reservation:
    return reservation_services.reservation_update(db, reservation_id, request)

@app.post("/reservations/{reservation_id}/cancel", response_model=schemas.ReservationResponse)
def reservation_cancel(reservation_id: int, db: Session = Depends(get_db)) -> models.Reservation:
    return reservation_services.reservation_cancel(db, reservation_id)

@app.post("/reservations/{reservation_id}/check-in", response_model=schemas.ReservationResponse)
def reservation_check_in(reservation_id: int, db: Session = Depends(get_db)) -> models.Reservation:
    return reservation_services.reservation_check_in(db, reservation_id)

@app.post("/reservations/{reservation_id}/check-out", response_model=schemas.ReservationResponse)
def reservation_check_out(reservation_id: int, db: Session = Depends(get_db)) -> models.Reservation:
    return reservation_services.reservation_check_out(db, reservation_id)

# --- REPORTS ---
# --- revenue ---
@app.post("/reports/revenue", response_model=schemas.RevenueReportResponse)
def revenue_report(request: schemas.RevenueReportRequest, db: Session = Depends(get_db)) -> schemas.RevenueReportResponse:
    revenue = report_services.revenue_report(db, request)
    return schemas.RevenueReportResponse(revenue=revenue)

@app.get("/reports/revenue/monthly", response_model=list[schemas.MonthlyRevenueReportResponse])
def revenue_report_monthly(db: Session = Depends(get_db)) -> list[schemas.MonthlyRevenueReportResponse]:
    return report_services.revenue_report_monthly(db)