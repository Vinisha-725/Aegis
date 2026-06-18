"""
Evidence model — raw data collected by the Argus agent.

One Evidence record per verification run, storing the raw
GitHub API response data as JSON.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from sqlalchemy import ForeignKey, Integer, JSON, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, generate_uuid

if TYPE_CHECKING:
    from app.models.milestone import Milestone


class Evidence(TimestampMixin, Base):
    """Raw evidence collected by Argus for a milestone verification run."""

    __tablename__ = "evidence"

    # ── Primary key ───────────────────────────────────────────────────────────
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)

    # ── Foreign keys ──────────────────────────────────────────────────────────
    milestone_id: Mapped[str] = mapped_column(
        ForeignKey("milestones.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ── Argus output ─────────────────────────────────────────────────────────
    evidence_found: Mapped[bool] = mapped_column(default=False, nullable=False)
    commits_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    files_changed: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    lines_added: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    lines_removed: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    pull_requests_merged: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    confidence: Mapped[float] = mapped_column(Numeric(precision=5, scale=4), default=0.0)

    # ── Raw payload (full GitHub API response for audit) ─────────────────────
    raw_commits: Mapped[list[Any] | None] = mapped_column(JSON, nullable=True)
    raw_pull_requests: Mapped[list[Any] | None] = mapped_column(JSON, nullable=True)
    raw_branches: Mapped[list[Any] | None] = mapped_column(JSON, nullable=True)

    # ── Relationships ─────────────────────────────────────────────────────────
    milestone: Mapped[Milestone] = relationship("Milestone", back_populates="evidence_records")

    def __repr__(self) -> str:
        return (
            f"<Evidence id={self.id!r} milestone={self.milestone_id!r} "
            f"confidence={self.confidence}>"
        )
