"""Pydantic schemas for the StockAlert resource."""

from datetime import datetime

from pydantic import BaseModel


class StockAlertCreate(BaseModel):
    """Schema for recording a new stock alert."""

    card_id: int
    retailer: str
    in_stock: bool
    url: str | None = None


class StockAlertRead(BaseModel):
    """Schema for reading a stock alert from the API."""

    id: int
    card_id: int
    retailer: str
    in_stock: bool
    url: str | None
    notified: bool
    detected_at: datetime

    model_config = {"from_attributes": True}
