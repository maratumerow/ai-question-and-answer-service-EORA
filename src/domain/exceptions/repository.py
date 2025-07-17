from typing import Any

from .base import DomainError


class RepositoryError(DomainError):
    """Базовая ошибка репозитория."""

    def __init__(
        self,
        message: str,
        original_error: Exception | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(message, **kwargs)
        self.original_error = original_error


class AnswerRepositoryError(RepositoryError):
    """Ошибка репозитория ответов."""


class QuestionRepositoryError(RepositoryError):
    """Ошибка репозитория вопросов."""


class SourceRepositoryError(RepositoryError):
    """Ошибка репозитория источников."""
