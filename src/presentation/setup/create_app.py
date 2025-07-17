import logging

from fastapi import FastAPI

from src.core.application.lifecycle import create_lifespan
from src.core.config import Settings
from src.core.logging import get_logger
from src.core.logging.config import setup_logging
from src.presentation.api.router import api_router
from src.presentation.setup import setup_exception_handlers, setup_middleware


def create_app(settings: Settings) -> FastAPI:
    """Фабрика создания приложения."""

    # Настройка логирования
    setup_logging(settings)
    logger = get_logger("app_factory")

    # Создание приложения
    app = _create_base_app(settings, logger)

    # Настройка middleware
    setup_middleware(app)

    # Подключение роутеров
    app.include_router(api_router, prefix=settings.api_str)

    # Настройка обработчиков ошибок (в конце)
    setup_exception_handlers(app)

    return app


def _create_base_app(settings: Settings, logger: logging.Logger) -> FastAPI:
    """Создание базового FastAPI приложения."""
    return FastAPI(
        title=settings.app_name,
        description=settings.description,
        version=settings.version,
        debug=settings.debug,
        lifespan=create_lifespan(logger, settings),
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
    )
