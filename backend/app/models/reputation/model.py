"""
models/reputation/model.py — Reputation domain model.

Tracks a user's cumulative performance score on the Aegis platform.
One Reputation record per User (1:1).
Updated after every ConsensusResult.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, generate_uuid

if TYPE_CHECKING:
    from app.models.user.model import User


class Reputation(TimestampMixin, Base):
    """Cumulative trust score for a user based on their verification history."""

    __tablename__ = "reputations"

    # ── Primary key ───────────────────────────────────────────────────────────
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)

    # ── Foreign key (unique → 1:1 with User) ──────────────────────────────────
    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    # ── Score ─────────────────────────────────────────────────────────────────
    overall_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    # overall_score: weighted average of all milestone quality scores (0.0–1.0)

    # ── Counters ──────────────────────────────────────────────────────────────
    total_milestones: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    successful_milestones: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False
    )
    failed_milestones: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    disputed_milestones: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_projects: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # ── Computed streak ───────────────────────────────────────────────────────
    current_streak: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    # consecutive successful milestones without a rejection

    # ── Badge / tier ─────────────────────────────────────────────────────────
    tier: Mapped[str] = mapped_column(String(20), default="newcomer", nullable=False)
    # tiers: newcomer → trusted → verified → elite

    # ── Notes (e.g. manually set by platform admin) ───────────────────────────
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # ── Relationship ──────────────────────────────────────────────────────────
    user: Mapped[User] = relationship("User", back_populates="reputation")

    def __repr__(self) -> str:
        return (
            f"<Reputation user={self.user_id!r} "
            f"score={self.overall_score:.2f} "
            f"tier={self.tier!r}>"
        )
