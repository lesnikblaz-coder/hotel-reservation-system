from sqlalchemy.orm import Session
from decimal import Decimal
from datetime import date

import repository

from models import Reservation

from schemas import RevenueReportRequest, MonthlyRevenueReportResponse, YearlyRevenueReportResponse, \
    OccupancyReportResponse, OccupancyReportRequest, MonthlyOccupancyReportResponse


def revenue_report(db: Session, data: RevenueReportRequest) -> Decimal:
    return repository.revenue_report(db, data) or Decimal("0")

def revenue_report_monthly(db: Session) -> list[MonthlyRevenueReportResponse]:
    rows = repository.revenue_report_monthly(db)

    return [
        MonthlyRevenueReportResponse(
            month=row.month.date(),
            revenue=row.revenue
        )
        for row in rows
    ]

def revenue_report_yearly(db: Session) -> list[YearlyRevenueReportResponse]:
    rows = repository.revenue_report_yearly(db)

    return [
        YearlyRevenueReportResponse(
            year=row.year.date(),
            revenue=row.revenue
        )
        for row in rows
    ]

def occupancy_report(db: Session) -> OccupancyReportResponse:
    total_rooms = repository.active_room_count(db)
    occupied_rooms = repository.get_occupied_rooms(db)
    occupancy_percentage = (
        round((occupied_rooms / total_rooms) * 100, 2)
        if total_rooms > 0
        else 0.0
    )

    return OccupancyReportResponse(
        total_rooms=total_rooms,
        occupied_rooms=occupied_rooms,
        occupancy_percentage=occupancy_percentage
    )

def occupancy_report_monthly(db: Session, data: OccupancyReportRequest) -> MonthlyOccupancyReportResponse:
    reservations = repository.reservations_for_month(db, data.month_start, data.month_end)

    total_occupied_nights: int = 0

    # for each reservation -> append total nights, if any in the selected month
    for r in reservations:
        total_occupied_nights += nights_in_month(
            r,
            data.month_start,
            data.month_end
        )

    # calculate total days in selected month
    total_days = (data.month_end - data.month_start).days

    # total available rooms * total days --> all total available nights
    available_room_nights = repository.active_room_count(db) * total_days

    if available_room_nights == 0:
        occupancy_percentage= 0.0
    else:
        occupancy_percentage = round((total_occupied_nights / available_room_nights) * 100, 2)

    return MonthlyOccupancyReportResponse(available_room_nights=available_room_nights, occupied_room_nights=total_occupied_nights, occupancy_percentage=occupancy_percentage)

def nights_in_month(reservation: Reservation, month_start: date, month_end: date) -> int:
    effective_start = max(reservation.check_in_date, month_start)
    effective_end = min(reservation.check_out_date, month_end)

    if effective_start >= effective_end:
        return 0

    return (effective_end - effective_start).days