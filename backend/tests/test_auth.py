"""
tests/test_auth.py — Unit tests verifying GitHub OAuth authentication routes and JWT session management.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import create_access_token
from app.core.database import get_db
from app.main import app
from app.models.user import User


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture(autouse=True)
def mock_db() -> AsyncMock:
    db = AsyncMock(spec=AsyncSession)

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    db.execute.return_value = mock_result

    async def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    yield db
    app.dependency_overrides.pop(get_db, None)


def test_auth_login_redirect(client: TestClient) -> None:
    # Set fake client ID
    with (
        patch("app.api.v1.auth.settings.github_client_id", "test-client-id"),
        patch(
            "app.api.v1.auth.settings.github_redirect_uri",
            "http://localhost:3000/auth/callback",
        ),
    ):
        response = client.get("/api/v1/auth/login", follow_redirects=False)
        assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
        redirect_url = response.headers.get("location")
        assert "github.com/login/oauth/authorize" in redirect_url
        assert "client_id=test-client-id" in redirect_url


@pytest.mark.asyncio
async def test_auth_callback_success(client: TestClient) -> None:
    # Mock settings
    with (
        patch("app.api.v1.auth.settings.github_client_id", "test-client-id"),
        patch("app.api.v1.auth.settings.github_client_secret", "test-client-secret"),
        patch(
            "app.api.v1.auth.settings.github_redirect_uri",
            "http://localhost:3000/auth/callback",
        ),
    ):
        mock_token_response = MagicMock()
        mock_token_response.is_success = True
        mock_token_response.json.return_value = {"access_token": "fake-github-token"}

        mock_user_response = MagicMock()
        mock_user_response.is_success = True
        mock_user_response.json.return_value = {
            "id": 1234567,
            "login": "test-github-user",
            "avatar_url": "https://avatars.githubusercontent.com/u/1234567",
            "name": "Test User",
            "bio": "Developer bio",
        }

        mock_email_response = MagicMock()
        mock_email_response.is_success = True
        mock_email_response.json.return_value = [
            {"email": "test@test.com", "primary": True, "verified": True}
        ]

        mock_user = User(
            id="test-uuid",
            github_id=1234567,
            github_username="test-github-user",
        )

        with (
            patch("httpx.AsyncClient.post", return_value=mock_token_response),
            patch("httpx.AsyncClient.get") as mock_get,
            patch("sqlalchemy.ext.asyncio.AsyncSession.execute") as mock_execute,
        ):
            mock_result = MagicMock()
            mock_result.scalar_one_or_none.return_value = mock_user
            mock_execute.return_value = mock_result

            mock_get.side_effect = [mock_user_response, mock_email_response]

            response = client.get("/api/v1/auth/callback?code=mock-code")
            assert response.status_code == status.HTTP_200_OK

            data = response.json()
            assert "access_token" in data
            assert data["token_type"] == "bearer"
            assert data["username"] == "test-github-user"


@pytest.mark.asyncio
async def test_auth_me_success(client: TestClient, mock_db: AsyncMock) -> None:
    # Need to verify we can access /me with generated token
    token = create_access_token(user_id="test-uuid")

    mock_user = User(
        id="test-uuid",
        github_id=123,
        github_username="test-github-user",
        github_email="test@test.com",
        github_avatar_url="https://avatar.png",
        display_name="Test User",
        bio="Test Bio",
    )

    with patch("app.core.dependencies.verify_access_token", return_value="test-uuid"):
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_user
        mock_db.execute.return_value = mock_result

        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/api/v1/auth/me", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == "test-uuid"
        assert data["github_username"] == "test-github-user"
        assert data["github_email"] == "test@test.com"
