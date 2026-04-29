"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-04-28

"""

from __future__ import annotations

from typing import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create cards, price_snapshots, and stock_alerts tables."""
    op.create_table(
        "cards",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("set_name", sa.String(255), nullable=False),
        sa.Column("card_number", sa.String(50), nullable=True),
        sa.Column("game", sa.String(50), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_cards_name", "cards", ["name"])

    op.create_table(
        "price_snapshots",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("card_id", sa.Integer(), nullable=False),
        sa.Column("source", sa.String(100), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("currency", sa.String(10), nullable=False, server_default="USD"),
        sa.Column(
            "recorded_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["card_id"], ["cards.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_price_snapshots_card_id", "price_snapshots", ["card_id"])
    op.create_index(
        "ix_price_snapshots_recorded_at", "price_snapshots", ["recorded_at"]
    )

    op.create_table(
        "stock_alerts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("card_id", sa.Integer(), nullable=False),
        sa.Column("retailer", sa.String(100), nullable=False),
        sa.Column("in_stock", sa.Boolean(), nullable=False),
        sa.Column("url", sa.String(1024), nullable=True),
        sa.Column("notified", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column(
            "detected_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["card_id"], ["cards.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_stock_alerts_card_id", "stock_alerts", ["card_id"])
    op.create_index("ix_stock_alerts_detected_at", "stock_alerts", ["detected_at"])


def downgrade() -> None:
    """Drop all tables."""
    op.drop_table("stock_alerts")
    op.drop_table("price_snapshots")
    op.drop_table("cards")
