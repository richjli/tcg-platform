"""Card model — represents a tracked TCG card."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.database import Base

if TYPE_CHECKING:
    from api.models.price_snapshot import PriceSnapshot
    from api.models.stock_alert import StockAlert


class Card(Base):
    """A tracked Pokémon or Riftbound card."""

    __tablename__ = "cards"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    set_name: Mapped[str] = mapped_column(String(255), nullable=False)
    card_number: Mapped[str | None] = mapped_column(String(50), nullable=True)
    game: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # "pokemon" | "riftbound"
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    price_snapshots: Mapped[list[PriceSnapshot]] = relationship(
        back_populates="card", cascade="all, delete-orphan"
    )
    stock_alerts: Mapped[list[StockAlert]] = relationship(
        back_populates="card", cascade="all, delete-orphan"
    )
