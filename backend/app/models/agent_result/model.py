"""
models/agent_result/model.py — AgentResult domain model.

Stores the structured output of a single AI agent run.
One row per (agent × milestone verification) pair.
"""

from __future__ import annotations

import enum
from typing import Any

from sqlalchemy import JSON, Enum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin, generate_uuid


class AgentName(enum.StrEnum):
    """Canonical identifiers for each Aegis verification agent."""

    ARGUS = "argus"
    THEMIS = "themis"
    DIKE = "dike"
    CHRONOS = "chronos"
    KRATOS = "kratos"


class AgentResult(TimestampMixin, Base):
    """
    Structured output produced by one agent during a verification run.

    score semantics per agent:
      argus   → confidence (0.0–1.0)
      themis  → scope_match (0.0–1.0)
      dike    → quality_score (0.0–1.0)
      chronos → None (boolean result; see output JSON for lateness_hours)
      kratos  → overall_score (0.0–1.0)
    """

    __tablename__ = "agent_results"

    # ── Primary key ───────────────────────────────────────────────────────────
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)

    # ── Foreign key ───────────────────────────────────────────────────────────
    milestone_id: Mapped[str] = mapped_column(
        ForeignKey("milestones.id", ondelete="CASCADE"), nullable=False, index=True
    )

    # ── Agent identity ────────────────────────────────────────────────────────
    agent_name: Mapped[AgentName] = mapped_column(
        Enum(AgentName, name="agent_name"), nullable=False, index=True
    )

    # ── Result ────────────────────────────────────────────────────────────────
    passed: Mapped[bool] = mapped_column(default=False, nullable=False)
    score: Mapped[float | None] = mapped_column(
        Numeric(precision=5, scale=4), nullable=True
    )
    reasoning: Mapped[str | None] = mapped_column(Text, nullable=True)

    # ── Full structured output (agent-specific schema) ────────────────────────
    output: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)

    # ── LLM metadata (Themis / Dike only) ────────────────────────────────────
    llm_model: Mapped[str | None] = mapped_column(String(100), nullable=True)
    llm_tokens_used: Mapped[int | None] = mapped_column(Integer, nullable=True)

    def __repr__(self) -> str:
        return (
            f"<AgentResult id={self.id!r} "
            f"agent={self.agent_name} "
            f"passed={self.passed} score={self.score}>"
        )
