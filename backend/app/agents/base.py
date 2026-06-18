"""
agents/base.py — Shared base classes for all Aegis verification agents.

Every agent:
  1. Receives a typed Pydantic input model
  2. Returns a typed Pydantic output model
  3. Raises AgentError on unrecoverable failures
"""

from __future__ import annotations

from pydantic import BaseModel


class AgentError(Exception):
    """Raised when an agent cannot complete its verification."""

    def __init__(self, agent: str, reason: str) -> None:
        self.agent = agent
        self.reason = reason
        super().__init__(f"[{agent}] {reason}")
