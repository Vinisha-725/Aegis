"""
models — Aegis domain models.

This file imports every model so SQLAlchemy's mapper registry
is fully populated when Alembic runs autogenerate.

Each domain has its own subfolder:
  base/            → Base, TimestampMixin, generate_uuid
  user/            → User
  project/         → Project, ProjectStatus
  milestone/       → Milestone, MilestoneStatus
  repository/      → Repository
  evidence/        → Evidence
  agent_result/    → AgentResult, AgentName
  consensus_result/→ ConsensusResult
  reputation/      → Reputation
"""

# ── Base (must be imported first) ─────────────────────────────────────────────
from app.models.agent_result import AgentName, AgentResult
from app.models.base import Base, TimestampMixin, generate_uuid
from app.models.consensus_result import ConsensusResult
from app.models.evidence import Evidence
from app.models.milestone import Milestone, MilestoneStatus
from app.models.project import Project, ProjectStatus
from app.models.repository import Repository
from app.models.reputation import Reputation

# ── Domain models ─────────────────────────────────────────────────────────────
from app.models.user import User

__all__ = [
    # Base
    "Base",
    "TimestampMixin",
    "generate_uuid",
    # Domain
    "User",
    "Project",
    "ProjectStatus",
    "Milestone",
    "MilestoneStatus",
    "Repository",
    "Evidence",
    "AgentResult",
    "AgentName",
    "ConsensusResult",
    "Reputation",
]
