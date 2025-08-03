from .base import BaseConfig
from .vector_search import VectorSearchConfig


class AppSettings(BaseConfig):
    """Основные настройки приложения."""

    # Основные настройки
    app_name: str = "EORA Q&A"
    title: str = "EORA Q&A Service"
    description: str = (
        "AI-powered question-answering service for EORA company cases"
    )
    debug: bool = True
    version: str = "0.1.0"

    # API настройки
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_str: str = "/api/v1"

    # Vector search settings
    vector_search: VectorSearchConfig = VectorSearchConfig()
