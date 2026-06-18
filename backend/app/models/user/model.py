"""
models/user/model.py — User domain model.

A User is any GitHub-authenticated person on the Aegis platform.
They can act as a project client (payer) or developer (payee).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, generate_uuid

if TYPE_CHECKING:
    from app.models.project.model import Project
    from app.models.reputation.model import Reputation


class User(TimestampMixin, Base):
    """Aegis platform user, authenticated via GitHub OAuth."""

    __tablename__ = "users"

    # ── Primary key ───────────────────────────────────────────────────────────
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)

    # ── GitHub identity ───────────────────────────────────────────────────────
    github_id: Mapped[int] = mapped_column(
        BigInteger, unique=True, nullable=False, index=True
    )
    github_username: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False
    )
    github_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    github_avatar_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    github_access_token: Mapped[str | None] = mapped_column(Text, nullable=True)

    # ── Profile ───────────────────────────────────────────────────────────────
    display_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # ── Relationships ─────────────────────────────────────────────────────────
    owned_projects: Mapped[list[Project]] = relationship(
        "Project",
        back_populates="client",
        foreign_keys="Project.client_id",
    )
    developer_projects: Mapped[list[Project]] = relationship(
        "Project",
        back_populates="developer",
        foreign_keys="Project.developer_id",
    )
    reputation: Mapped[Reputation | None] = relationship(
        "Reputation",
        back_populates="user",
        uselist=False,
    )

    def __repr__(self) -> str:
        return f"<User id={self.id!r} github={self.github_username!r}>"
