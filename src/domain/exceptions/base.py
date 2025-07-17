from abc import ABC
from typing import Any


class DomainError(Exception, ABC):
    """Базовое доменное исключение."""

    def __init__(
        self,
        message: str,
        *,
        error_code: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.error_code = error_code or self.__class__.__name__
        self.details = details or {}

    def __str__(self) -> str:
        return self.message

    def to_dict(self) -> dict[str, Any]:
        """Преобразование исключения в словарь для JSON ответа."""
        return {
            "error": self.error_code,
            "message": self.message,
            "details": self.details,
        }


class ValidationError(DomainError):
    """Ошибка валидации данных."""

    def __init__(
        self,
        message: str = "Ошибка валидации данных",
        *,
        field: str | None = None,
        value: Any = None,
        **kwargs: Any,
    ) -> None:
        details = kwargs.pop("details", {})
        if field:
            details["field"] = field
        if value is not None:
            details["value"] = value
        super().__init__(message, details=details, **kwargs)


class NotFoundError(DomainError):
    """Ошибка - ресурс не найден."""

    def __init__(
        self,
        message: str = "Ресурс не найден",
        *,
        resource_type: str | None = None,
        resource_id: Any = None,
        **kwargs: Any,
    ) -> None:
        details = kwargs.pop("details", {})
        if resource_type:
            details["resource_type"] = resource_type
        if resource_id is not None:
            details["resource_id"] = str(resource_id)
        super().__init__(message, details=details, **kwargs)


class ConflictError(DomainError):
    """Ошибка конфликта - ресурс уже существует."""

    def __init__(
        self,
        message: str = "Конфликт данных",
        *,
        resource_type: str | None = None,
        conflicting_value: Any = None,
        **kwargs: Any,
    ) -> None:
        details = kwargs.pop("details", {})
        if resource_type:
            details["resource_type"] = resource_type
        if conflicting_value is not None:
            details["conflicting_value"] = str(conflicting_value)
        super().__init__(message, details=details, **kwargs)


class UnauthorizedError(DomainError):
    """Ошибка авторизации."""

    def __init__(
        self,
        message: str = "Не авторизован",
        **kwargs: Any,
    ) -> None:
        super().__init__(message, **kwargs)


class ForbiddenError(DomainError):
    """Ошибка доступа - недостаточно прав."""

    def __init__(
        self,
        message: str = "Недостаточно прав доступа",
        *,
        required_permission: str | None = None,
        **kwargs: Any,
    ) -> None:
        details = kwargs.pop("details", {})
        if required_permission:
            details["required_permission"] = required_permission
        super().__init__(message, details=details, **kwargs)


class BusinessRuleViolationError(DomainError):
    """Ошибка нарушения бизнес-правила."""

    def __init__(
        self,
        message: str,
        *,
        rule_name: str | None = None,
        **kwargs: Any,
    ) -> None:
        details = kwargs.pop("details", {})
        if rule_name:
            details["rule_name"] = rule_name
        super().__init__(message, details=details, **kwargs)
