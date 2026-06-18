"""
agents/themis — Scope validation agent.

Themis uses Claude to compare the milestone requirements
against the actual repository changes.

Input:  { milestone, acceptance_criteria, commits, files_changed, commit_messages }
Output: { scope_match }  — float 0.0–1.0
"""

from app.agents.themis.agent import ThemisAgent, ThemisInput, ThemisOutput

__all__ = ["ThemisAgent", "ThemisInput", "ThemisOutput"]
