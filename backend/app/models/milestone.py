"""
models/milestone/model.py — Milestone domain model.

A Milestone is a single deliverable within a Project.
It has acceptance criteria, a deadline, and flows through a verification
lifecycle that culminates in a Kratos consensus decision.
"""

from __future__ import annotations

import enum
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, generate_uuid

if TYPE_CHECKING:
    from app.models.consensus_result import ConsensusResult
    from app.models.evidence import Evidence
    from app.models.project import Project


class MilestoneStatus(enum.StrEnum):
    """Full lifecycle of a single milestone."""

    PENDING = "pending"  # Defined, not yet started
    IN_PROGRESS = "in_progress"  # Developer is working
    SUBMITTED = "submitted"  # Developer submitted for review
    VERIFYING = "verifying"  # Aegis agents running
    APPROVED = "approved"  # Consensus passed — payment triggered
    REJECTED = "rejected"  # Consensus failed
    DISPUTED = "disputed"  # Under appeal (Nemesis — future phase)


class Milestone(TimestampMixin, Base):
    """A discrete deliverable unit within a Project."""

    __tablename__ = "milestones"

    # ── Primary key ───────────────────────────────────────────────────────────
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)

    # ── Foreign key ───────────────────────────────────────────────────────────
    project_id: Mapped[str] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )

    # ── Content ───────────────────────────────────────────────────────────────
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    acceptance_criteria: Mapped[str | None] = mapped_column(Text, nullable=True)
    order_index: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # ── Payment ───────────────────────────────────────────────────────────────
    payment_amount: Mapped[float | None] = mapped_column(
        Numeric(precision=18, scale=6), nullable=True
    )
    payment_token: Mapped[str] = mapped_column(
        String(10), default="USDC", nullable=False
    )

    # ── Scheduling ────────────────────────────────────────────────────────────
    deadline: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    submitted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # ── Status ────────────────────────────────────────────────────────────────
    status: Mapped[MilestoneStatus] = mapped_column(
        Enum(MilestoneStatus, name="milestone_status"),
        default=MilestoneStatus.PENDING,
        nullable=False,
        index=True,
    )

    # ── Relationships ─────────────────────────────────────────────────────────
    project: Mapped[Project] = relationship("Project", back_populates="milestones")
    evidence_records: Mapped[list[Evidence]] = relationship(
        "Evidence",
        back_populates="milestone",
        cascade="all, delete-orphan",
    )
    consensus_result: Mapped[ConsensusResult | None] = relationship(
        "ConsensusResult",
        back_populates="milestone",
        uselist=False,
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Milestone id={self.id!r} title={self.title!r} status={self.status}>"
