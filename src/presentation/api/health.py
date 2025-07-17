import logging

from fastapi import APIRouter

from src.core.config import get_settings

router = APIRouter()
settings = get_settings()
logger = logging.getLogger(__name__)


@router.get("/")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""

    logger.info("Health check endpoint called")
    return {
        "status": "healthy",
        "service": settings.app_name,
    }
