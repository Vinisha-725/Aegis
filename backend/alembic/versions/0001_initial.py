"""initial empty migration — Phase 0 foundation

Revision ID: 0001_initial
Revises:
Create Date: 2026-06-18

No tables yet. Domain models are added in Phase 1.
"""

from __future__ import annotations

from collections.abc import Sequence

revision: str = "0001_initial"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Phase 0: no schema changes. Tables created in Phase 1."""
    pass


def downgrade() -> None:
    """Phase 0: nothing to roll back."""
    pass
