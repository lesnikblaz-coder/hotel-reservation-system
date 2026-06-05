from sqlalchemy.orm import Session
from decimal import Decimal

import repository

from schemas import RevenueReportRequest

def revenue_report(db: Session, data: RevenueReportRequest) -> Decimal:
    return repository.revenue_report(db, data) or Decimal("0")