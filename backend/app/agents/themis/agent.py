"""
agents/themis/agent.py — Acceptance criteria checking agent.

Themis asks Claude Haiku to compare:
  - What the milestone requires (description + acceptance criteria)
  - What was actually done (commits, files changed, commit messages)

and scores how well they match.

Input:
    milestone            → milestone title
    acceptance_criteria  → acceptance criteria text (may be None)
    commits              → commit count from Argus
    files_changed        → file count from Argus
    commit_messages      → list of commit message summaries from Argus

Output:
    scope_match  → float 0.0–1.0
                   (Claude scores 0–100, we divide by 100)
"""

from __future__ import annotations

import json
import re

import anthropic
from pydantic import BaseModel

from app.agents.base import AgentError

# ── I/O schemas ───────────────────────────────────────────────────────────────


class ThemisInput(BaseModel):
    """Input to the Themis scope validation agent."""

    milestone: str
    acceptance_criteria: str | None = None
    commits: int
    files_changed: int
    commit_messages: list[str] = []


class ThemisOutput(BaseModel):
    """Themis scope validation output."""

    scope_match: float  # 0.0–1.0


# ── Prompt template ───────────────────────────────────────────────────────────

_PROMPT = """\
You are an expert software project reviewer assessing milestone completion.

## Milestone
{milestone}

## Acceptance Criteria
{criteria}

## What Was Done
- Commits: {commits}
- Files changed: {files_changed}
- Commit messages:
{messages}

## Task
Score how well the repository changes satisfy the milestone requirements.
Consider: completeness, relevance of changed files, and commit message alignment.

Respond with ONLY valid JSON — no explanation, no markdown:
{{"scope_match": <integer 0-100>}}
"""

# ── Agent ─────────────────────────────────────────────────────────────────────


class ThemisAgent:
    """
    Uses Claude Haiku to score scope alignment between a milestone
    definition and the evidence collected by Argus.
    """

    _DEFAULT_MODEL = "claude-haiku-4-5"
    _MAX_TOKENS = 64
    _MAX_MESSAGES = 15  # trim commit list to keep prompt concise

    def __init__(self, api_key: str, model: str = _DEFAULT_MODEL) -> None:
        self._client = anthropic.AsyncAnthropic(api_key=api_key)
        self._model = model

    # ── Public interface ──────────────────────────────────────────────────────

    async def run(self, input: ThemisInput) -> ThemisOutput:
        """Score scope match between milestone requirements and Argus evidence."""
        prompt = self._build_prompt(input)
        raw_score = await self._call_claude(prompt)
        scope_match = round(raw_score / 100, 4)
        return ThemisOutput(scope_match=scope_match)

    # ── Private helpers ───────────────────────────────────────────────────────

    def _build_prompt(self, input: ThemisInput) -> str:
        messages = input.commit_messages[: self._MAX_MESSAGES]
        formatted = "\n".join(f"  - {m}" for m in messages) or "  (none)"
        return _PROMPT.format(
            milestone=input.milestone,
            criteria=input.acceptance_criteria or "Not specified",
            commits=input.commits,
            files_changed=input.files_changed,
            messages=formatted,
        )

    async def _call_claude(self, prompt: str) -> float:
        """Call Claude and parse the scope_match integer from its response."""
        try:
            message = await self._client.messages.create(
                model=self._model,
                max_tokens=self._MAX_TOKENS,
                messages=[{"role": "user", "content": prompt}],
            )
        except anthropic.APIError as e:
            raise AgentError("themis", f"Anthropic API error: {e}") from e

        text = message.content[0].text.strip()
        return self._parse_score(text)

    @staticmethod
    def _parse_score(text: str) -> float:
        """Extract scope_match integer from Claude's JSON response."""
        try:
            # Try direct JSON parse first
            data = json.loads(text)
            return float(data["scope_match"])
        except (json.JSONDecodeError, KeyError):
            pass

        # Fallback: extract first number from the text
        match = re.search(r"\d+(?:\.\d+)?", text)
        if match:
            return float(match.group())

        raise AgentError("themis", f"Could not parse scope_match from: {text!r}")
