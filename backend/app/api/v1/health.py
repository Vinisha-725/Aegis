import datetime

from fastapi import APIRouter

from app.shared.config import get_settings

router = APIRouter()
settings = get_settings()


@router.get("/health", tags=["system"])
async def health_check() -> dict:
    """Health check — returns service status, environment, and current timestamp."""
    return {
        "status": "ok",
        "service": "aegis-backend",
        "environment": settings.environment,
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
    }
