"""
tests/test_agents.py — Unit tests for verification agents.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.agents.argus.agent import ArgusAgent, ArgusInput
from app.agents.base import AgentError
from app.agents.dike.agent import DikeAgent, DikeInput
from app.agents.kratos.agent import KratosAgent, KratosInput
from app.agents.themis.agent import ThemisAgent, ThemisInput

# ── Argus Agent Tests ─────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_argus_agent_success() -> None:
    agent = ArgusAgent(github_token="fake-token")

    mock_commits_response = [
        {"sha": "sha1", "commit": {"message": "feat: add first feature"}},
        {"sha": "sha256", "commit": {"message": "fix: resolve critical bug"}},
    ]

    mock_files_response = {
        "files": [{"filename": "app/main.py"}, {"filename": "tests/test_main.py"}]
    }

    with patch("httpx.AsyncClient.get") as mock_get:
        # Mock first call to commits list, then calls to individual commits for files
        mock_response_commits = MagicMock()
        mock_response_commits.status_code = 200
        mock_response_commits.is_success = True
        mock_response_commits.json.return_value = mock_commits_response

        mock_response_files = MagicMock()
        mock_response_files.status_code = 200
        mock_response_files.is_success = True
        mock_response_files.json.return_value = mock_files_response

        mock_get.side_effect = [
            mock_response_commits,
            mock_response_files,
            mock_response_files,
        ]

        inp = ArgusInput(repo="owner/repo", milestone="Build Landing Page")
        out = await agent.run(inp)

        assert out.evidence_found is True
        assert out.commits == 2
        assert out.files_changed == 2
        assert out.commit_messages == [
            "feat: add first feature",
            "fix: resolve critical bug",
        ]
        assert out.file_list == ["app/main.py", "tests/test_main.py"]
        # commit_score = min(1.0, 2/10) = 0.2
        # file_score = min(1.0, 2/10) = 0.2
        # confidence = 0.2 * 0.6 + 0.2 * 0.4 = 0.2
        assert out.confidence == 0.2


@pytest.mark.asyncio
async def test_argus_agent_not_found() -> None:
    agent = ArgusAgent(github_token="fake-token")

    with patch("httpx.AsyncClient.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.is_success = False
        mock_get.return_value = mock_response

        inp = ArgusInput(repo="owner/repo", milestone="Build Landing Page")
        with pytest.raises(AgentError) as excinfo:
            await agent.run(inp)

        assert "not found" in str(excinfo.value)


# ── Themis Agent Tests ────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_themis_agent_success() -> None:
    agent = ThemisAgent(api_key="fake-key")

    mock_message = MagicMock()
    mock_message.content = [MagicMock(text='{"scope_match": 85}')]

    with patch(
        "anthropic.AsyncAnthropic.messages", new_callable=PropertyMock
    ) as mock_messages_prop:
        mock_messages = AsyncMock()
        mock_messages.create.return_value = mock_message
        mock_messages_prop.return_value = mock_messages

        inp = ThemisInput(
            milestone="Build Login Page",
            acceptance_criteria="User can sign in",
            commits=3,
            files_changed=2,
            commit_messages=["feat: oauth flow", "feat: login page ui"],
        )
        out = await agent.run(inp)

        assert out.scope_match == 0.85


# ── Dike Agent Tests ──────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_dike_agent_success() -> None:
    agent = DikeAgent(api_key="fake-key")

    mock_message = MagicMock()
    mock_message.content = [MagicMock(text='{"quality": 92}')]

    with patch(
        "anthropic.AsyncAnthropic.messages", new_callable=PropertyMock
    ) as mock_messages_prop:
        mock_messages = AsyncMock()
        mock_messages.create.return_value = mock_message
        mock_messages_prop.return_value = mock_messages

        inp = DikeInput(
            milestone="Build Login Page",
            acceptance_criteria="User can sign in",
            commits=3,
            files_changed=2,
            commit_messages=["feat: oauth flow", "feat: login page ui"],
            file_list=["app/auth.py", "tests/test_auth.py"],
        )
        out = await agent.run(inp)

        assert out.quality == 92


# ── Kratos Agent Tests ────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_kratos_agent_approved() -> None:
    agent = KratosAgent(threshold=75)

    inp = KratosInput(
        argus_confidence=0.8,
        scope_match=0.9,
        quality=85,
    )
    out = await agent.run(inp)

    # Convert all to 0-100 scale
    # argus: 80, themis: 90, dike: 85
    # weighted: 90 * 0.5 + 85 * 0.3 + 80 * 0.2 = 45 + 25.5 + 16 = 86.5 -> rounds to 86 (banker's rounding)
    assert out.confidence == 86
    assert out.approved is True


@pytest.mark.asyncio
async def test_kratos_agent_rejected() -> None:
    agent = KratosAgent(threshold=75)

    inp = KratosInput(
        argus_confidence=0.4,
        scope_match=0.5,
        quality=60,
    )
    out = await agent.run(inp)

    # themis: 50 * 0.5 = 25
    # dike: 60 * 0.3 = 18
    # argus: 40 * 0.2 = 8
    # weighted: 25 + 18 + 8 = 51
    assert out.confidence == 51
    assert out.approved is False


# Helper property mock for Anthropic client mock
class PropertyMock(MagicMock):
    def __get__(self, obj, objtype):
        return self()
