import logging
import time
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI

from src.core.config import Settings


def create_lifespan(logger: logging.Logger, settings: Settings) -> Any:
    """Создает lifespan функцию для конкретного приложения."""

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        # Startup
        start_time = time.time()
        app.state.start_time = start_time

        try:
            logger.info("🚀 EORA Q&A сервис запущен")
            logger.info("🔧 Debug режим: %s", settings.debug)
            logger.info("🌐 API доступно на: %s", settings.api_str)

            # Здесь можно добавить инициализацию БД, кеша и т.д.

            yield

        except Exception as e:
            logger.error(f"❌ Ошибка при запуске приложения: {e}")
            raise
        finally:
            # Shutdown
            uptime = time.time() - app.state.start_time
            logger.info(
                "⏹️ EORA Q&A сервис остановлен (время работы: %.2f сек)", uptime
            )

    return lifespan
