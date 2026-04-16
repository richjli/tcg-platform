"""StockAlert model — records when a card is in stock at a retailer."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.database import Base

if TYPE_CHECKING:
    from api.models.card import Card


class StockAlert(Base):
    """A stock availability event for a card at a specific retailer."""

    __tablename__ = "stock_alerts"

    id: Mapped[int] = mapped_column(primary_key=True)
    card_id: Mapped[int] = mapped_column(
        ForeignKey("cards.id"), nullable=False, index=True
    )
    retailer: Mapped[str] = mapped_column(String(100), nullable=False)  # e.g. "target"
    in_stock: Mapped[bool] = mapped_column(Boolean, nullable=False)
    url: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    notified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    detected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True
    )

    card: Mapped[Card] = relationship(back_populates="stock_alerts")
