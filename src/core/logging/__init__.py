import logging

from .config import setup_logging


def get_logger(name: str) -> logging.Logger:
    """Получить логгер для модуля."""
    return logging.getLogger(f"src.{name}")


__all__ = [
    "get_logger",
    "setup_logging",
]
