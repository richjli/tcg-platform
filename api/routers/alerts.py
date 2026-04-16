"""Stock alerts router."""

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.database import get_db
from api.models.stock_alert import StockAlert
from api.schemas.stock_alert import StockAlertRead

router = APIRouter(prefix="/alerts", tags=["alerts"])

DB = Annotated[Session, Depends(get_db)]


@router.get("/", response_model=list[StockAlertRead])
def list_alerts(db: DB, unnotified_only: bool = False) -> list[StockAlert]:
    """Return stock alerts, optionally filtered to unnotified ones."""
    q = db.query(StockAlert).order_by(StockAlert.detected_at.desc())
    if unnotified_only:
        q = q.filter(StockAlert.notified == False)  # noqa: E712
    return q.all()
