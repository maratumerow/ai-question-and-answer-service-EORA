from pydantic import Field

from .base import BaseConfig


class DatabaseSettings(BaseConfig):
    """Настройки базы данных."""

    database_url: str = Field(
        default="postgresql+asyncpg://user:password@localhost:5432/eora_db",
        description="URL для подключения к базе данных",
    )
    pool_pre_ping: bool = Field(
        default=True, description="Проверять соединение перед использованием"
    )
    pool_recycle: int = Field(
        default=3000, description="Пересоздавать соединения каждые 50 минут"
    )

    @property
    def alembic_database_url(self) -> str:
        """URL для Alembic (синхронный)"""
        return self.database_url.replace("+asyncpg", "")
