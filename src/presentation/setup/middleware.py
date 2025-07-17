from fastapi import FastAPI

from src.core.middleware.logging import logging_middleware


def setup_middleware(app: FastAPI) -> None:
    """Настройка middleware."""
    # Middleware для логирования
    app.middleware("http")(logging_middleware)
