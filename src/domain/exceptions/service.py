from typing import Any

from .base import DomainError


class ServiceError(DomainError):
    """Base class for service-related errors."""

    def __init__(
        self,
        message: str,
        original_error: Exception | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(message, **kwargs)
        self.original_error = original_error


class LLMServiceError(ServiceError):
    """Exception raised by LLM service."""

    def __init__(
        self,
        message: str,
        original_error: Exception | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(message, original_error=original_error, **kwargs)


class ContentParsingServiceError(ServiceError):
    """Exception raised by content parsing service."""

    def __init__(
        self,
        message: str,
        original_error: Exception | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(message, original_error=original_error, **kwargs)


class SourceMatchingServiceError(ServiceError):
    """Exception raised by source matching service."""

    def __init__(
        self,
        message: str,
        original_error: Exception | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(message, original_error=original_error, **kwargs)
