"""Cards router."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.database import get_db
from api.models.card import Card
from api.schemas.card import CardCreate, CardRead

router = APIRouter(prefix="/cards", tags=["cards"])

DB = Annotated[Session, Depends(get_db)]


@router.get("/", response_model=list[CardRead])
def list_cards(db: DB) -> list[Card]:
    """Return all tracked cards."""
    return db.query(Card).order_by(Card.name).all()


@router.get("/{card_id}", response_model=CardRead)
def get_card(card_id: int, db: DB) -> Card:
    """Return a single card by ID."""
    card = db.get(Card, card_id)
    if card is None:
        raise HTTPException(status_code=404, detail="Card not found")
    return card


@router.post("/", response_model=CardRead, status_code=201)
def create_card(payload: CardCreate, db: DB) -> Card:
    """Create a new tracked card."""
    card = Card(**payload.model_dump())
    db.add(card)
    db.commit()
    db.refresh(card)
    return card
