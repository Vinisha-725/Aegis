from datetime import UTC, datetime

from fastapi import APIRouter

from app.core.config import get_settings

router = APIRouter()
settings = get_settings()


@router.get("/health", tags=["system"])
async def health_check() -> dict:
    """Health check endpoint. Returns service status and environment info."""
    return {
        "status": "ok",
        "service": "aegis-backend",
        "environment": settings.environment,
        "timestamp": datetime.now(UTC).isoformat(),
    }
