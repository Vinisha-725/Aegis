"""
models/base — Shared SQLAlchemy base and mixins.

Exports Base, TimestampMixin, generate_uuid for use by all domain models.
"""

from app.models.base.model import Base, TimestampMixin, generate_uuid

__all__ = ["Base", "TimestampMixin", "generate_uuid"]
