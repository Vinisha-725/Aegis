"""
models/repository/model.py — Repository domain model.

Stores GitHub repository metadata for a Project.
One project → one repository (1:1).
Stats are cached locally and refreshed on sync (Phase 4).
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, generate_uuid

if TYPE_CHECKING:
    from app.models.project.model import Project


class Repository(TimestampMixin, Base):
    """A GitHub repository connected 1:1 to an Aegis project."""

    __tablename__ = "repositories"

    # ── Primary key ───────────────────────────────────────────────────────────
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)

    # ── Foreign key (unique → 1:1 with Project) ───────────────────────────────
    project_id: Mapped[str] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    # ── GitHub metadata ───────────────────────────────────────────────────────
    github_repo_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(512), nullable=False)  # owner/repo
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    clone_url: Mapped[str] = mapped_column(Text, nullable=False)
    default_branch: Mapped[str] = mapped_column(
        String(255), default="main", nullable=False
    )
    is_private: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # ── Cached stats (refreshed by Phase 4 GitHub sync) ──────────────────────
    stars_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    forks_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    open_issues_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_synced_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # ── Relationships ─────────────────────────────────────────────────────────
    project: Mapped[Project] = relationship("Project", back_populates="repository")

    def __repr__(self) -> str:
        return f"<Repository id={self.id!r} full_name={self.full_name!r}>"
