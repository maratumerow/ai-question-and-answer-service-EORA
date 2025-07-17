from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):
    """Базовые настройки для всех конфигураций."""

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Игнорируем дополнительные поля из .env
