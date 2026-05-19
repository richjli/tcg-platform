"""initial

Revision ID: 0001
Revises:
Create Date: 2026-05-18

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0001"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "cards",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("set_name", sa.String(length=255), nullable=False),
        sa.Column("card_number", sa.String(length=50), nullable=True),
        sa.Column("game", sa.String(length=50), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_cards_name"), "cards", ["name"], unique=False)

    op.create_table(
        "price_snapshots",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("card_id", sa.Integer(), nullable=False),
        sa.Column("source", sa.String(length=100), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("currency", sa.String(length=10), nullable=False),
        sa.Column(
            "recorded_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["card_id"], ["cards.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_price_snapshots_card_id"), "price_snapshots", ["card_id"], unique=False
    )
    op.create_index(
        op.f("ix_price_snapshots_recorded_at"),
        "price_snapshots",
        ["recorded_at"],
        unique=False,
    )

    op.create_table(
        "stock_alerts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("card_id", sa.Integer(), nullable=False),
        sa.Column("retailer", sa.String(length=100), nullable=False),
        sa.Column("in_stock", sa.Boolean(), nullable=False),
        sa.Column("url", sa.String(length=1024), nullable=True),
        sa.Column("notified", sa.Boolean(), nullable=False),
        sa.Column(
            "detected_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["card_id"], ["cards.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_stock_alerts_card_id"), "stock_alerts", ["card_id"], unique=False
    )
    op.create_index(
        op.f("ix_stock_alerts_detected_at"),
        "stock_alerts",
        ["detected_at"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_stock_alerts_detected_at"), table_name="stock_alerts")
    op.drop_index(op.f("ix_stock_alerts_card_id"), table_name="stock_alerts")
    op.drop_table("stock_alerts")

    op.drop_index(op.f("ix_price_snapshots_recorded_at"), table_name="price_snapshots")
    op.drop_index(op.f("ix_price_snapshots_card_id"), table_name="price_snapshots")
    op.drop_table("price_snapshots")

    op.drop_index(op.f("ix_cards_name"), table_name="cards")
    op.drop_table("cards")
