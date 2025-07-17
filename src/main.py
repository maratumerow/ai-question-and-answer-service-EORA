from dotenv import load_dotenv
from fastapi import FastAPI

from src.core.config import get_settings
from src.presentation.setup.create_app import create_app

load_dotenv()


def initialize_app() -> FastAPI:
    """Инициализация приложения."""
    settings = get_settings()
    return create_app(settings)


# Создание приложения
app = initialize_app()
