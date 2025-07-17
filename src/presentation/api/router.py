from fastapi import APIRouter

from .health import router as health_router
from .load_source import router as load_source_router
from .question import router as question_router

# Создание основного роутера для API
api_router = APIRouter()

# Подключение роутеров

api_router.include_router(
    health_router,
    prefix="/health",
    tags=["Health Check"],
)
api_router.include_router(
    load_source_router,
    prefix="/sources",
    tags=["Source Management"],
)
api_router.include_router(
    question_router,
    prefix="/questions",
    tags=["Q&A"],
)
