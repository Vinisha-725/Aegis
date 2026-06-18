"""
ConsensusResult model — Kratos engine final verdict for a milestone.

Stores the aggregated decision from all four agents and whether
the escrow release was triggered.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from sqlalchemy import Boolean, ForeignKey, JSON, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, generate_uuid

if TYPE_CHECKING:
    from app.models.milestone import Milestone


class ConsensusResult(TimestampMixin, Base):
    """Kratos consensus engine output for a single milestone verification."""

    __tablename__ = "consensus_results"

    # ── Primary key ───────────────────────────────────────────────────────────
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)

    # ── Foreign keys (one-to-one with Milestone) ──────────────────────────────
    milestone_id: Mapped[str] = mapped_column(
        ForeignKey("milestones.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    # ── Per-agent pass/fail ───────────────────────────────────────────────────
    argus_passed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    themis_passed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    dike_passed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    chronos_on_time: Mapped[bool] = mapped_column(Boolean, nullable=False)

    # ── Per-agent scores ──────────────────────────────────────────────────────
    argus_confidence: Mapped[float | None] = mapped_column(Numeric(5, 4), nullable=True)
    themis_scope_match: Mapped[float | None] = mapped_column(Numeric(5, 4), nullable=True)
    dike_quality_score: Mapped[float | None] = mapped_column(Numeric(5, 4), nullable=True)
    chronos_lateness_hours: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)

    # ── Final verdict ────────────────────────────────────────────────────────
    approved: Mapped[bool] = mapped_column(Boolean, nullable=False)
    overall_score: Mapped[float | None] = mapped_column(Numeric(5, 4), nullable=True)
    reasoning: Mapped[str | None] = mapped_column(Text, nullable=True)
    escrow_release_triggered: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # ── Full snapshot of all agent outputs (for audit) ────────────────────────
    agent_outputs_snapshot: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)

    # ── Relationships ─────────────────────────────────────────────────────────
    milestone: Mapped[Milestone] = relationship(
        "Milestone", back_populates="consensus_result"
    )

    def __repr__(self) -> str:
        return (
            f"<ConsensusResult id={self.id!r} milestone={self.milestone_id!r} "
            f"approved={self.approved}>"
        )
