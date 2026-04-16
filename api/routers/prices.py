"""Prices router."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.database import get_db
from api.models.card import Card
from api.models.price_snapshot import PriceSnapshot
from api.schemas.price_snapshot import PriceSnapshotCreate, PriceSnapshotRead

router = APIRouter(prefix="/prices", tags=["prices"])

DB = Annotated[Session, Depends(get_db)]


@router.get("/", response_model=list[PriceSnapshotRead])
def list_prices(
    db: DB, card_id: int | None = None, limit: int = 100
) -> list[PriceSnapshot]:
    """Return price snapshots, optionally filtered by card."""
    q = db.query(PriceSnapshot).order_by(PriceSnapshot.recorded_at.desc())
    if card_id is not None:
        q = q.filter(PriceSnapshot.card_id == card_id)
    return q.limit(limit).all()


@router.post("/", response_model=PriceSnapshotRead, status_code=201)
def record_price(payload: PriceSnapshotCreate, db: DB) -> PriceSnapshot:
    """Record a new price snapshot for a card."""
    if db.get(Card, payload.card_id) is None:
        raise HTTPException(status_code=404, detail="Card not found")
    snapshot = PriceSnapshot(**payload.model_dump())
    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)
    return snapshot
