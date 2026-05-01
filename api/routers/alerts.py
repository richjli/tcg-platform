"""Stock alerts router."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.database import get_db
from api.models.card import Card
from api.models.stock_alert import StockAlert
from api.schemas.stock_alert import StockAlertCreate, StockAlertRead

router = APIRouter(prefix="/alerts", tags=["alerts"])

DB = Annotated[Session, Depends(get_db)]


@router.get("/", response_model=list[StockAlertRead])
def list_alerts(db: DB, unnotified_only: bool = False) -> list[StockAlert]:
    """Return stock alerts, optionally filtered to unnotified ones."""
    q = db.query(StockAlert).order_by(StockAlert.detected_at.desc())
    if unnotified_only:
        q = q.filter(StockAlert.notified == False)  # noqa: E712
    return q.all()


@router.post("/", response_model=StockAlertRead, status_code=201)
def record_alert(payload: StockAlertCreate, db: DB) -> StockAlert:
    """Record a new stock alert for a card."""
    if db.get(Card, payload.card_id) is None:
        raise HTTPException(status_code=404, detail="Card not found")
    alert = StockAlert(**payload.model_dump())
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert
