from pydantic import Field

from .base import BaseConfig


class LoggingSettings(BaseConfig):
    """Настройки логирования."""

    log_level: str = Field(
        default="INFO",
        description="Уровень логирования (DEBUG, INFO, WARNING, ERROR)",
    )
    log_file_enabled: bool = Field(
        default=True, description="Включить логирование в файл"
    )
    log_json_format: bool = Field(
        default=False, description="Использовать JSON формат для логов"
    )

    # Дополнительные настройки логирования
    log_rotation: str = Field(
        default="midnight", description="Ротация логов (midnight, size:10MB)"
    )
    log_retention: int = Field(
        default=30, description="Количество дней хранения логов"
    )
