"""Pydantic schemas for the PriceSnapshot resource."""

from datetime import datetime

from pydantic import BaseModel


class PriceSnapshotCreate(BaseModel):
    """Schema for recording a new price snapshot."""

    card_id: int
    source: str
    price: float
    currency: str = "USD"


class PriceSnapshotRead(BaseModel):
    """Schema for reading a price snapshot from the API."""

    id: int
    card_id: int
    source: str
    price: float
    currency: str
    recorded_at: datetime

    model_config = {"from_attributes": True}
