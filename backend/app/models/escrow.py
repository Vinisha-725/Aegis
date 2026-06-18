"""
Escrow model — tracks a Solana escrow account for a Milestone payment.

In Phase 11 this links to an actual on-chain account.
For now it stores the intent and simulated state.
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
    from app.models.user import User


class EscrowStatus(str, enum.Enum):
    """Lifecycle status of an escrow account."""

    PENDING = "pending"       # Awaiting funding
    FUNDED = "funded"         # On-chain account funded
    RELEASED = "released"     # Payment sent to payee
    REFUNDED = "refunded"     # Payment returned to payer
    DISPUTED = "disputed"     # Under dispute (Nemesis — future)


class Escrow(TimestampMixin, Base):
    """
    Represents a Solana escrow account holding payment for a milestone.
    One escrow per milestone.
    """

    __tablename__ = "escrows"

    # ── Primary key ───────────────────────────────────────────────────────────
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)

    # ── Foreign keys ──────────────────────────────────────────────────────────
    milestone_id: Mapped[str] = mapped_column(
        ForeignKey("milestones.id", ondelete="RESTRICT"),
        unique=True,
        nullable=False,
        index=True,
    )
    payer_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    payee_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    # ── Payment ───────────────────────────────────────────────────────────────
    amount: Mapped[float] = mapped_column(Numeric(precision=18, scale=6), nullable=False)
    token: Mapped[str] = mapped_column(String(10), default="USDC", nullable=False)
    status: Mapped[EscrowStatus] = mapped_column(
        Enum(EscrowStatus, name="escrow_status"),
        default=EscrowStatus.PENDING,
        nullable=False,
        index=True,
    )

    # ── Solana on-chain data (Phase 11) ───────────────────────────────────────
    solana_account_address: Mapped[str | None] = mapped_column(String(64), nullable=True)
    solana_tx_fund: Mapped[str | None] = mapped_column(String(128), nullable=True)
    solana_tx_release: Mapped[str | None] = mapped_column(String(128), nullable=True)
    solana_network: Mapped[str] = mapped_column(String(20), default="devnet", nullable=False)

    # ── Timestamps ────────────────────────────────────────────────────────────
    funded_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    released_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # ── Notes ────────────────────────────────────────────────────────────────
    release_notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # ── Relationships ─────────────────────────────────────────────────────────
    milestone: Mapped[Milestone] = relationship("Milestone", back_populates="escrow")
    payer: Mapped[User] = relationship(
        "User", back_populates="escrows_as_payer", foreign_keys=[payer_id]
    )
    payee: Mapped[User] = relationship(
        "User", back_populates="escrows_as_payee", foreign_keys=[payee_id]
    )

    def __repr__(self) -> str:
        return (
            f"<Escrow id={self.id!r} milestone={self.milestone_id!r} "
            f"amount={self.amount} status={self.status}>"
        )
