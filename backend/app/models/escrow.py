"""
models/escrow.py — Escrow domain model.

Tracks Solana escrow account deployments and payment states for Milestones.
One Milestone has one Escrow (1:1).
"""

from __future__ import annotations

import enum
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, generate_uuid

if TYPE_CHECKING:
    from app.models.milestone import Milestone


class EscrowStatus(enum.StrEnum):
    """Solana smart contract escrow state."""

    PENDING = "pending"  # Created locally, not yet funded on-chain
    FUNDED = "funded"  # USDC deposited on Solana escrow program
    RELEASED = "released"  # USDC paid out to developer
    REFUNDED = "refunded"  # USDC returned to client (appeal/cancel)


class Escrow(TimestampMixin, Base):
    """An escrow payment associated 1:1 with a Project Milestone."""

    __tablename__ = "escrows"

    # ── Primary key ───────────────────────────────────────────────────────────
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)

    # ── Foreign key (1:1 with Milestone) ──────────────────────────────────────
    milestone_id: Mapped[str] = mapped_column(
        ForeignKey("milestones.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    # ── Blockchain Details ───────────────────────────────────────────────────
    escrow_address: Mapped[str | None] = mapped_column(
        String(255), nullable=True
    )  # Solana PDA pubkey
    amount: Mapped[float] = mapped_column(
        Numeric(precision=18, scale=6), nullable=False
    )
    token: Mapped[str] = mapped_column(String(10), default="USDC", nullable=False)
    status: Mapped[EscrowStatus] = mapped_column(
        Enum(EscrowStatus, name="escrow_status"),
        default=EscrowStatus.PENDING,
        nullable=False,
    )

    # ── Audit Trail ───────────────────────────────────────────────────────────
    tx_signature: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )  # Last on-chain txn sig
    funded_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    released_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    refunded_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # ── Relationship ──────────────────────────────────────────────────────────
    milestone: Mapped[Milestone] = relationship("Milestone", back_populates="escrow")

    def __repr__(self) -> str:
        return (
            f"<Escrow id={self.id!r} "
            f"milestone={self.milestone_id!r} "
            f"amount={self.amount} "
            f"status={self.status}>"
        )
