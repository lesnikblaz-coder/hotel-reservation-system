from sqlalchemy.orm import Session
from decimal import Decimal

import repository

from schemas import RevenueReportRequest, MonthlyRevenueReportResponse, YearlyRevenueReportResponse, OccupancyReportResponse


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
    total_rooms = repository.get_total_rooms(db)
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