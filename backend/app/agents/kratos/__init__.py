"""
agents/kratos — Consensus agent.

Kratos consumes all upstream agent outputs and produces a final approval decision and consensus confidence.

Input:  { argus_confidence, scope_match, quality }
Output: { approved, confidence }
"""

from __future__ import annotations

from app.agents.kratos.agent import KratosAgent, KratosInput, KratosOutput

__all__ = ["KratosAgent", "KratosInput", "KratosOutput"]
