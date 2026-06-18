"""
models/base/model.py — Shared SQLAlchemy base, mixins, and helpers.

All domain models inherit from Base and optionally TimestampMixin.
"""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Shared declarative base inherited by all Aegis ORM models."""

    pass


class TimestampMixin:
    """
    Adds created_at and updated_at columns to any model.

    created_at: set once on INSERT via server default
    updated_at: refreshed on every UPDATE via server default + onupdate
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


def generate_uuid() -> str:
    """Return a new UUID4 string — used as default for primary keys."""
    return str(uuid.uuid4())


# ── Public API of this module ─────────────────────────────────────────────────
__all__ = ["Base", "TimestampMixin", "generate_uuid"]
