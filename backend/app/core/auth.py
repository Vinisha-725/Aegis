"""
core/auth.py — Authentication utility functions (JWT generation and validation).
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from jose import JWTError, jwt

from app.core.config import get_settings

settings = get_settings()


def create_access_token(user_id: str) -> str:
    """Generate a JWT access token containing the user_id as 'sub' claim."""
    expire = datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode = {
        "sub": user_id,
        "exp": expire,
    }
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def verify_access_token(token: str) -> str | None:
    """Decode and validate a JWT access token. Return user_id if valid, else None."""
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        user_id: str | None = payload.get("sub")
        if user_id is None:
            return None
        return user_id
    except JWTError:
        return None
