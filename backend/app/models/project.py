"""
models/project/model.py — Project domain model.

A Project is a contract between a client (payer) and a developer (payee).
It groups one or more Milestones and links to a GitHub Repository.
"""

from __future__ import annotations

import enum
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, generate_uuid

if TYPE_CHECKING:
    from app.models.milestone import Milestone
    from app.models.repository import Repository
    from app.models.user import User


class ProjectStatus(enum.StrEnum):
    """Lifecycle status of a project."""

    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Project(TimestampMixin, Base):
    """A client–developer contract containing milestones and a linked repo."""

    __tablename__ = "projects"

    # ── Primary key ───────────────────────────────────────────────────────────
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)

    # ── Content ───────────────────────────────────────────────────────────────
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[ProjectStatus] = mapped_column(
        Enum(ProjectStatus, name="project_status"),
        default=ProjectStatus.DRAFT,
        nullable=False,
    )

    # ── Parties ───────────────────────────────────────────────────────────────
    client_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    developer_id: Mapped[str | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )

    # ── Relationships ─────────────────────────────────────────────────────────
    client: Mapped[User] = relationship(
        "User", back_populates="owned_projects", foreign_keys=[client_id]
    )
    developer: Mapped[User | None] = relationship(
        "User", back_populates="developer_projects", foreign_keys=[developer_id]
    )
    milestones: Mapped[list[Milestone]] = relationship(
        "Milestone",
        back_populates="project",
        cascade="all, delete-orphan",
        order_by="Milestone.order_index",
    )
    repository: Mapped[Repository | None] = relationship(
        "Repository",
        back_populates="project",
        uselist=False,
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Project id={self.id!r} title={self.title!r} status={self.status}>"
