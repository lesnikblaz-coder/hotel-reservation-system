from sqlalchemy.orm import Session
from decimal import Decimal

import repository

from schemas import RevenueReportRequest, MonthlyRevenueReportResponse, YearlyRevenueReportResponse


def revenue_report(db: Session, data: RevenueReportRequest) -> Decimal:
    return repository.revenue_report(db, data) or Decimal("0")

def revenue_report_monthly(db: Session):
    rows = repository.revenue_report_monthly(db)

    return [
        MonthlyRevenueReportResponse(
            month=row.month.date(),
            revenue=row.revenue
        )
        for row in rows
    ]

def revenue_report_yearly(db: Session):
    rows = repository.revenue_report_yearly(db)

    return [
        YearlyRevenueReportResponse(
            year=row.year.date(),
            revenue=row.revenue
        )
        for row in rows
    ]