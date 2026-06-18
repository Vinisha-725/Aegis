"""
AgentResult model — stores the output of a single AI agent run.

One AgentResult row per (agent, milestone_verification) pair.
"""

from __future__ import annotations

import enum
from typing import Any

from sqlalchemy import Enum, ForeignKey, JSON, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, generate_uuid


class AgentName(str, enum.Enum):
    """Identifiers for each Aegis verification agent."""

    ARGUS = "argus"
    THEMIS = "themis"
    DIKE = "dike"
    CHRONOS = "chronos"
    KRATOS = "kratos"


class AgentResult(TimestampMixin, Base):
    """
    The structured output produced by a single agent during
    a milestone verification run.
    """

    __tablename__ = "agent_results"

    # ── Primary key ───────────────────────────────────────────────────────────
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)

    # ── Foreign keys ──────────────────────────────────────────────────────────
    milestone_id: Mapped[str] = mapped_column(
        ForeignKey("milestones.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ── Agent identity ────────────────────────────────────────────────────────
    agent_name: Mapped[AgentName] = mapped_column(
        Enum(AgentName, name="agent_name"),
        nullable=False,
        index=True,
    )

    # ── Common fields ─────────────────────────────────────────────────────────
    passed: Mapped[bool] = mapped_column(default=False, nullable=False)
    score: Mapped[float | None] = mapped_column(
        Numeric(precision=5, scale=4), nullable=True
    )  # main numeric output (confidence / scope_match / quality_score / etc.)
    reasoning: Mapped[str | None] = mapped_column(Text, nullable=True)

    # ── Full structured output (agent-specific keys) ──────────────────────────
    output: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)

    # ── LLM metadata (Themis / Dike) ─────────────────────────────────────────
    llm_model: Mapped[str | None] = mapped_column(String(100), nullable=True)
    llm_tokens_used: Mapped[int | None] = mapped_column(nullable=True)

    def __repr__(self) -> str:
        return (
            f"<AgentResult id={self.id!r} agent={self.agent_name} "
            f"passed={self.passed} score={self.score}>"
        )
