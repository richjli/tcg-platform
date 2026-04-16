"""PriceSnapshot model — a price observation for a card at a point in time."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Float, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.database import Base

if TYPE_CHECKING:
    from api.models.card import Card


class PriceSnapshot(Base):
    """A recorded price for a card from a specific source."""

    __tablename__ = "price_snapshots"

    id: Mapped[int] = mapped_column(primary_key=True)
    card_id: Mapped[int] = mapped_column(
        ForeignKey("cards.id"), nullable=False, index=True
    )
    source: Mapped[str] = mapped_column(String(100), nullable=False)  # e.g. "tcgplayer"
    price: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="USD")
    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True
    )

    card: Mapped[Card] = relationship(back_populates="price_snapshots")
