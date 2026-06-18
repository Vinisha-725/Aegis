"""
agents/dike — Quality evaluation agent.

Dike uses Claude to evaluate:
  - Complexity
  - Test coverage
  - Documentation

Input:  { milestone, acceptance_criteria, commits, files_changed, commit_messages, file_list }
Output: { quality }
"""

from __future__ import annotations

from app.agents.dike.agent import DikeAgent, DikeInput, DikeOutput

__all__ = ["DikeAgent", "DikeInput", "DikeOutput"]
