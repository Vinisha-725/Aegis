"""Add escrow model

Revision ID: b650309b9e29
Revises: 0002_domain_models
Create Date: 2026-06-18 18:00:04.838972+00:00

"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b650309b9e29"
down_revision: str | None = "0002_domain_models"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    escrow_status = sa.Enum(
        "pending", "funded", "released", "refunded", name="escrow_status"
    )
    op.create_table(
        "escrows",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "milestone_id",
            sa.String(36),
            sa.ForeignKey("milestones.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        ),
        sa.Column("escrow_address", sa.String(255), nullable=True),
        sa.Column("amount", sa.Numeric(18, 6), nullable=False),
        sa.Column("token", sa.String(10), nullable=False, server_default="USDC"),
        sa.Column("status", escrow_status, nullable=False, server_default="pending"),
        sa.Column("tx_signature", sa.Text(), nullable=True),
        sa.Column("funded_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("released_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("refunded_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_index("ix_escrows_milestone_id", "escrows", ["milestone_id"], unique=True)


def downgrade() -> None:
    op.drop_table("escrows")
    op.execute("DROP TYPE IF EXISTS escrow_status")
