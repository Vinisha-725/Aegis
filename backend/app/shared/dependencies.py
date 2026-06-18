"""
shared/dependencies.py — Reusable FastAPI dependency functions.

These are injected into route handlers via Depends().
Add auth dependencies here in Phase 2.
"""

from __future__ import annotations

from app.shared.database import get_db

__all__ = ["get_db"]
