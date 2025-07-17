from functools import lru_cache
from typing import Any

from .app import AppSettings
from .database import DatabaseSettings
from .llm import LLMConfig
from .logging import LoggingSettings


class Settings(AppSettings, DatabaseSettings, LoggingSettings, LLMConfig):
    """Объединенные настройки приложения."""

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)


@lru_cache
def get_settings() -> Settings:
    """Получить настройки приложения (с кешированием)."""
    return Settings()


__all__ = ["get_settings"]
