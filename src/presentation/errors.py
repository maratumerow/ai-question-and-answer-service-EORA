import traceback

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.core.logging import get_logger
from src.domain.exceptions import (
    ConflictError,
    DomainError,
    ForbiddenError,
    NotFoundError,
    ValidationError,
)

logger = get_logger("api.errors")


def unified_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    """Универсальный обработчик всех исключений."""

    # Доменные исключения
    if isinstance(exc, DomainError):
        logger.warning(
            "Domain error on %s %s: %s",
            request.method,
            request.url,
            exc.message,
        )

        # Определяем HTTP статус код на основе типа исключения
        if isinstance(exc, ValidationError):
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        elif isinstance(exc, NotFoundError):
            status_code = status.HTTP_404_NOT_FOUND
        elif isinstance(exc, ConflictError):
            status_code = status.HTTP_409_CONFLICT
        elif isinstance(exc, ForbiddenError):
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        else:
            # Для остальных доменных ошибок используем 400
            status_code = status.HTTP_400_BAD_REQUEST

        return JSONResponse(
            status_code=status_code,
            content=exc.to_dict(),
        )

    # Ошибки валидации FastAPI
    if isinstance(exc, RequestValidationError):
        logger.warning(
            "Validation error on %s %s: %s",
            request.method,
            request.url,
            exc.errors(),
        )
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "detail": "Ошибка валидации данных",
                "errors": exc.errors(),
            },
        )

    # HTTP исключения Starlette
    if isinstance(exc, StarletteHTTPException):
        logger.info(
            "HTTP %d on %s %s: %s",
            exc.status_code,
            request.method,
            request.url,
            exc.detail,
        )
        return JSONResponse(
            status_code=exc.status_code, content={"detail": exc.detail}
        )

    # Все остальные исключения
    logger.error(
        "Unexpected error on %s %s: %s\n%s",
        request.method,
        request.url,
        str(exc),
        traceback.format_exc(),
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Внутренняя ошибка сервера"},
    )


def general_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    """Обработчик общих ошибок."""
    logger.error(
        "Unexpected error on %s %s: %s\n%s",
        request.method,
        request.url,
        str(exc),
        traceback.format_exc(),
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Внутренняя ошибка сервера"},
    )
