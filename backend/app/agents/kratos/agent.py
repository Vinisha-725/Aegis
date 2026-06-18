"""
agents/kratos/agent.py — Consensus engine agent.

Kratos aggregates findings from:
  - Argus (GitHub verification confidence)
  - Themis (Scope match score)
  - Dike (Quality score)

and calculates:
  1. approved: bool (consensus threshold met)
  2. confidence: int (0-100 overall confidence score)

Input:
    argus_confidence  → float 0.0-1.0
    scope_match       → float 0.0-1.0
    quality           → int 0-100

Output:
    approved    → bool
    confidence  → int 0-100
"""

from __future__ import annotations

from pydantic import BaseModel


class KratosInput(BaseModel):
    """Input to the Kratos consensus agent."""

    argus_confidence: float  # 0.0 - 1.0
    scope_match: float  # 0.0 - 1.0
    quality: int  # 0 - 100


class KratosOutput(BaseModel):
    """Kratos consensus engine output."""

    approved: bool
    confidence: int  # 0 - 100


class KratosAgent:
    """Consensus engine aggregating upstream agent evaluations."""

    def __init__(self, threshold: int = 70) -> None:
        self._threshold = threshold

    async def run(self, input: KratosInput) -> KratosOutput:
        """
        Consolidates upstream evaluations using a weighted formula.

        Weights:
            - Themis (scope_match): 50%
            - Dike (quality): 30%
            - Argus (argus_confidence): 20%
        """
        # Convert all to 0-100 scale
        argus_pct = input.argus_confidence * 100
        themis_pct = input.scope_match * 100
        dike_pct = float(input.quality)

        weighted_confidence = (
            (themis_pct * 0.50) + (dike_pct * 0.30) + (argus_pct * 0.20)
        )
        confidence = int(round(weighted_confidence))

        # Clamp between 0 and 100
        confidence = max(0, min(100, confidence))
        approved = confidence >= self._threshold

        return KratosOutput(approved=approved, confidence=confidence)
