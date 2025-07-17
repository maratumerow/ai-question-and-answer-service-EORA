import logging
import logging.config
import sys
from pathlib import Path
from typing import Any

from src.core.config import Settings


def setup_logging(settings: Settings) -> None:
    """Настройка системы логирования."""

    # Создаем директорию для логов
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Конфигурация логирования
    logging_config: dict[str, Any] = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": (
                    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                ),
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "detailed": {
                "format": (
                    "%(asctime)s - %(name)s - %(levelname)s - %(module)s - "
                    "%(funcName)s:%(lineno)d - %(message)s"
                ),
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "json": {
                "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                "format": (
                    "%(asctime)s %(name)s %(levelname)s %(module)s "
                    "%(funcName)s %(lineno)d %(message)s"
                ),
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "INFO" if not settings.debug else "DEBUG",
                "formatter": "default",
                "stream": sys.stdout,
            },
            "file_info": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "detailed",
                "filename": "logs/eora.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
                "encoding": "utf8",
            },
            "file_error": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "ERROR",
                "formatter": "detailed",
                "filename": "logs/eora_errors.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
                "encoding": "utf8",
            },
        },
        "loggers": {
            # Корневой логгер приложения
            "src": {
                "level": "DEBUG" if settings.debug else "INFO",
                "handlers": ["console", "file_info", "file_error"],
                "propagate": False,
            },
            # Логгер для API
            "src.api": {
                "level": "DEBUG" if settings.debug else "INFO",
                "handlers": ["console", "file_info"],
                "propagate": False,
            },
            # Логгер для базы данных
            "src.infrastructure.database": {
                "level": "DEBUG" if settings.debug else "WARNING",
                "handlers": ["console", "file_info"],
                "propagate": False,
            },
            # Логгер для бизнес-логики
            "src.use_cases": {
                "level": "DEBUG" if settings.debug else "INFO",
                "handlers": ["console", "file_info"],
                "propagate": False,
            },
            # Внешние библиотеки
            "sqlalchemy.engine": {
                "level": "WARNING" if not settings.debug else "INFO",
                "handlers": ["console"],
                "propagate": False,
            },
            "uvicorn": {
                "level": "INFO",
                "handlers": ["console"],
                "propagate": False,
            },
            "fastapi": {
                "level": "INFO",
                "handlers": ["console"],
                "propagate": False,
            },
        },
        "root": {
            "level": "WARNING",
            "handlers": ["console"],
        },
    }

    logging.config.dictConfig(logging_config)
