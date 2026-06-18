"""
agents/dike/agent.py — Quality evaluation agent.

Dike asks Claude Haiku to evaluate:
  - Complexity
  - Test coverage
  - Documentation

and outputs a quality score between 0 and 100.

Input:
    milestone            → milestone title
    acceptance_criteria  → acceptance criteria text (may be None)
    commits              → commit count from Argus
    files_changed        → file count from Argus
    commit_messages      → list of commit message summaries from Argus
    file_list            → list of files changed from Argus

Output:
    quality  → int 0–100
"""

from __future__ import annotations

import json
import re

import anthropic
from pydantic import BaseModel

from app.agents.base import AgentError

# ── I/O schemas ───────────────────────────────────────────────────────────────


class DikeInput(BaseModel):
    """Input to the Dike quality evaluation agent."""

    milestone: str
    acceptance_criteria: str | None = None
    commits: int
    files_changed: int
    commit_messages: list[str] = []
    file_list: list[str] = []


class DikeOutput(BaseModel):
    """Dike quality evaluation output."""

    quality: int  # 0–100


# ── Prompt template ───────────────────────────────────────────────────────────

_PROMPT = """\
You are an expert software quality and repository auditor.
Analyze the following evidence of work for a given milestone:

## Milestone
{milestone}

## Acceptance Criteria
{criteria}

## Repository Changes
- Commits: {commits}
- Files changed: {files_changed}
- Commit messages:
{messages}
- File list:
{file_list}

## Task
Evaluate the quality of the work based on three dimensions:
1. Complexity: Does the file list and commit history show substantial effort, proper architecture, and correct scoping?
2. Test coverage: Is there evidence of tests being added or modified (e.g., test files, spec files, or testing-related commits)?
3. Documentation: Are there updates to documentation (e.g., Markdown files, README, or docstrings)?

Score the overall quality on a scale of 0 to 100.

Respond with ONLY valid JSON — no explanation, no markdown:
{{"quality": <integer 0-100>}}
"""

# ── Agent ─────────────────────────────────────────────────────────────────────


class DikeAgent:
    """
    Uses Claude Haiku to evaluate complexity, test coverage, and documentation
    based on the evidence collected by Argus.
    """

    _DEFAULT_MODEL = "claude-haiku-4-5"
    _MAX_TOKENS = 64
    _MAX_ITEMS = 15  # trim lists to keep prompt concise

    def __init__(self, api_key: str, model: str = _DEFAULT_MODEL) -> None:
        self._client = anthropic.AsyncAnthropic(api_key=api_key)
        self._model = model

    # ── Public interface ──────────────────────────────────────────────────────

    async def run(self, input: DikeInput) -> DikeOutput:
        """Evaluate project quality based on milestone requirements and Argus evidence."""
        prompt = self._build_prompt(input)
        quality_score = await self._call_claude(prompt)
        return DikeOutput(quality=quality_score)

    # ── Private helpers ───────────────────────────────────────────────────────

    def _build_prompt(self, input: DikeInput) -> str:
        messages = input.commit_messages[: self._MAX_ITEMS]
        formatted_messages = "\n".join(f"  - {m}" for m in messages) or "  (none)"

        files = input.file_list[: self._MAX_ITEMS]
        formatted_files = "\n".join(f"  - {f}" for f in files) or "  (none)"

        return _PROMPT.format(
            milestone=input.milestone,
            criteria=input.acceptance_criteria or "Not specified",
            commits=input.commits,
            files_changed=input.files_changed,
            messages=formatted_messages,
            file_list=formatted_files,
        )

    async def _call_claude(self, prompt: str) -> int:
        """Call Claude and parse the quality integer from its response."""
        try:
            message = await self._client.messages.create(
                model=self._model,
                max_tokens=self._MAX_TOKENS,
                messages=[{"role": "user", "content": prompt}],
            )
        except anthropic.APIError as e:
            raise AgentError("dike", f"Anthropic API error: {e}") from e

        text = message.content[0].text.strip()
        return self._parse_score(text)

    @staticmethod
    def _parse_score(text: str) -> int:
        """Extract quality integer from Claude's JSON response."""
        try:
            # Try direct JSON parse first
            data = json.loads(text)
            return int(float(data["quality"]))
        except (json.JSONDecodeError, KeyError, ValueError):
            pass

        # Fallback: extract first number from the text
        match = re.search(r"\d+", text)
        if match:
            return int(match.group())

        raise AgentError("dike", f"Could not parse quality from: {text!r}")
