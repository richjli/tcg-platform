"""Pydantic schemas for the Card resource."""

from datetime import datetime

from pydantic import BaseModel


class CardCreate(BaseModel):
    """Schema for creating a new card."""

    name: str
    set_name: str
    card_number: str | None = None
    game: str


class CardRead(BaseModel):
    """Schema for reading a card from the API."""

    id: int
    name: str
    set_name: str
    card_number: str | None
    game: str
    created_at: datetime

    model_config = {"from_attributes": True}
