"""
agents/argus/agent.py — GitHub verification agent.

Argus verifies that real work exists in a repository by querying
the GitHub REST API for commits and changed files.

Input:
    repo      → "owner/repo"
    milestone → milestone title (used for context, not filtering)
    since     → ISO 8601 datetime — start of evidence window
    until     → ISO 8601 datetime — end of evidence window (submission time)

Output:
    evidence_found  → bool   — True if any commits were found
    commits         → int    — number of commits in the window
    files_changed   → int    — number of unique files touched
    confidence      → float  — 0.0–1.0, derived from commit and file counts

Internal (passed to Themis / Dike via pipeline):
    commit_messages → list[str]
    file_list       → list[str]
"""

from __future__ import annotations

import httpx
from pydantic import BaseModel

from app.agents.base import AgentError

# ── I/O schemas ───────────────────────────────────────────────────────────────


class ArgusInput(BaseModel):
    """Input to the Argus GitHub verification agent."""

    repo: str  # "owner/repo"
    milestone: str  # milestone title — logged for traceability
    since: str | None = None  # ISO 8601 — start of evidence window
    until: str | None = None  # ISO 8601 — end of evidence window


class ArgusOutput(BaseModel):
    """
    Argus verification output.

    Public fields (returned to caller):
        evidence_found, commits, files_changed

    Pipeline fields (forwarded to Themis / Dike):
        confidence, commit_messages, file_list
    """

    # ── Public output ─────────────────────────────────────────────────────────
    evidence_found: bool
    commits: int
    files_changed: int

    # ── Pipeline metadata (used internally, stored in Evidence table) ─────────
    confidence: float  # 0.0–1.0
    commit_messages: list[str] = []
    file_list: list[str] = []


# ── Agent ────────────────────────────────────────────────────────────────────


class ArgusAgent:
    """
    Queries the GitHub REST API to collect evidence of work within a date range.

    Confidence formula:
        commit_score = min(1.0, commits / 10)   ← saturates at 10 commits
        file_score   = min(1.0, files  / 10)    ← saturates at 10 files
        confidence   = commit_score × 0.6 + file_score × 0.4
    """

    _GITHUB_API = "https://api.github.com"
    _COMMITS_PER_PAGE = 100
    _FILES_SAMPLE_SIZE = 5   # max commits to inspect for file lists
    _CONFIDENCE_COMMIT_TARGET = 10
    _CONFIDENCE_FILE_TARGET = 10

    def __init__(self, github_token: str) -> None:
        self._token = github_token

    # ── Public interface ──────────────────────────────────────────────────────

    async def run(self, input: ArgusInput) -> ArgusOutput:
        """Run GitHub verification for the given repo and milestone window."""
        headers = {
            "Authorization": f"Bearer {self._token}",
            "Accept": "application/vnd.github.v3+json",
        }

        async with httpx.AsyncClient(headers=headers, timeout=30.0) as client:
            commits_data = await self._fetch_commits(client, input)
            commit_messages = self._extract_messages(commits_data)
            file_list = await self._fetch_changed_files(client, input.repo, commits_data)

        commits_count = len(commits_data)
        files_count = len(file_list)
        evidence_found = commits_count > 0
        confidence = self._compute_confidence(commits_count, files_count)

        return ArgusOutput(
            evidence_found=evidence_found,
            commits=commits_count,
            files_changed=files_count,
            confidence=confidence,
            commit_messages=commit_messages,
            file_list=file_list,
        )

    # ── Private helpers ───────────────────────────────────────────────────────

    async def _fetch_commits(
        self, client: httpx.AsyncClient, input: ArgusInput
    ) -> list[dict]:
        """Fetch commits in the evidence window from the GitHub API."""
        params: dict[str, str | int] = {"per_page": self._COMMITS_PER_PAGE}
        if input.since:
            params["since"] = input.since
        if input.until:
            params["until"] = input.until

        response = await client.get(
            f"{self._GITHUB_API}/repos/{input.repo}/commits", params=params
        )

        if response.status_code == 404:
            raise AgentError("argus", f"Repository '{input.repo}' not found or not accessible.")
        if not response.is_success:
            raise AgentError("argus", f"GitHub API error {response.status_code}.")

        data = response.json()
        return data if isinstance(data, list) else []

    @staticmethod
    def _extract_messages(commits_data: list[dict]) -> list[str]:
        """Extract commit messages from raw GitHub commit objects."""
        messages = []
        for commit in commits_data:
            msg = commit.get("commit", {}).get("message", "").splitlines()[0]
            if msg:
                messages.append(msg)
        return messages

    async def _fetch_changed_files(
        self, client: httpx.AsyncClient, repo: str, commits_data: list[dict]
    ) -> list[str]:
        """Collect unique file paths changed across a sample of commits."""
        file_set: set[str] = set()

        for commit in commits_data[: self._FILES_SAMPLE_SIZE]:
            sha = commit.get("sha", "")
            if not sha:
                continue
            response = await client.get(f"{self._GITHUB_API}/repos/{repo}/commits/{sha}")
            if response.is_success:
                for f in response.json().get("files", []):
                    filename = f.get("filename", "")
                    if filename:
                        file_set.add(filename)

        return sorted(file_set)

    def _compute_confidence(self, commits: int, files: int) -> float:
        """Return a 0.0–1.0 confidence score from commit and file counts."""
        commit_score = min(1.0, commits / self._CONFIDENCE_COMMIT_TARGET)
        file_score = min(1.0, files / self._CONFIDENCE_FILE_TARGET)
        return round(commit_score * 0.6 + file_score * 0.4, 4)
