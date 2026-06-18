"""
api/v1/auth.py — Authentication routes (GitHub OAuth & session management).
"""

from __future__ import annotations

import httpx
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import create_access_token
from app.core.config import get_settings
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.reputation import Reputation
from app.models.user import User

router = APIRouter()
settings = get_settings()

_GITHUB_OAUTH_URL = "https://github.com/login/oauth"
_GITHUB_API_URL = "https://api.github.com"


@router.get("/login", tags=["auth"])
async def github_login() -> RedirectResponse:
    """Redirect user to GitHub to authorize Aegis."""
    if not settings.github_client_id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="GitHub Client ID is not configured.",
        )

    oauth_url = (
        f"{_GITHUB_OAUTH_URL}/authorize"
        f"?client_id={settings.github_client_id}"
        f"&redirect_uri={settings.github_redirect_uri}"
        f"&scope=user:email"
    )
    return RedirectResponse(url=oauth_url)


@router.get("/callback", tags=["auth"])
async def github_callback(
    code: str = Query(..., description="The authorization code from GitHub"),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    Handle the GitHub redirect callback, exchange code for access token,
    upsert user profile, and issue a local JWT session token.
    """
    # ── 1. Exchange authorization code for GitHub access token ────────────────
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            f"{_GITHUB_OAUTH_URL}/access_token",
            data={
                "client_id": settings.github_client_id,
                "client_secret": settings.github_client_secret,
                "code": code,
                "redirect_uri": settings.github_redirect_uri,
            },
            headers={"Accept": "application/json"},
            timeout=15.0,
        )

        if not token_response.is_success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to retrieve access token from GitHub.",
            )

        token_data = token_response.json()
        github_token = token_data.get("access_token")
        if not github_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"GitHub OAuth error: {token_data.get('error_description', 'No access token returned')}",
            )

        # ── 2. Retrieve GitHub user profile ───────────────────────────────────
        headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Aegis-Auth-Service",
        }
        user_response = await client.get(
            f"{_GITHUB_API_URL}/user", headers=headers, timeout=10.0
        )
        if not user_response.is_success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to fetch user profile from GitHub.",
            )
        user_profile = user_response.json()

        # ── 3. Retrieve user email ────────────────────────────────────────────
        email_response = await client.get(
            f"{_GITHUB_API_URL}/user/emails", headers=headers, timeout=10.0
        )
        email = None
        if email_response.is_success:
            emails = email_response.json()
            # Find primary email
            for e in emails:
                if e.get("primary") and e.get("verified"):
                    email = e.get("email")
                    break
            if not email and emails:
                email = emails[0].get("email")

    github_id = user_profile["id"]
    username = user_profile["login"]

    # ── 4. Upsert User in local database ──────────────────────────────────────
    result = await db.execute(select(User).where(User.github_id == github_id))
    user = result.scalar_one_or_none()

    if user is None:
        user = User(
            github_id=github_id,
            github_username=username,
            github_email=email,
            github_avatar_url=user_profile.get("avatar_url"),
            github_access_token=github_token,
            display_name=user_profile.get("name"),
            bio=user_profile.get("bio"),
        )
        db.add(user)
        await db.flush()  # Generate user.id

        # Also create empty reputation record
        reputation = Reputation(user_id=user.id)
        db.add(reputation)
    else:
        # Update profile details and token
        user.github_username = username
        if email:
            user.github_email = email
        user.github_avatar_url = user_profile.get("avatar_url")
        user.github_access_token = github_token
        user.display_name = user_profile.get("name")
        user.bio = user_profile.get("bio")

    await db.commit()

    # ── 5. Generate Aegis session JWT token ───────────────────────────────────
    access_token = create_access_token(user_id=user.id)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": username,
    }


@router.get("/me", tags=["auth"])
async def read_current_user(current_user: User = Depends(get_current_user)) -> dict:
    """Return profile details for the currently authenticated user."""
    return {
        "id": current_user.id,
        "github_username": current_user.github_username,
        "github_email": current_user.github_email,
        "github_avatar_url": current_user.github_avatar_url,
        "display_name": current_user.display_name,
        "bio": current_user.bio,
        "created_at": current_user.created_at.isoformat()
        if current_user.created_at
        else None,
    }
