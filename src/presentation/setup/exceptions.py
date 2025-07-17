from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.domain.exceptions.base import DomainError
from src.presentation.errors import unified_exception_handler


def setup_exception_handlers(app: FastAPI) -> None:
    """Настройка обработчиков ошибок."""

    # 1. Доменные ошибки (самые специфичные)
    app.add_exception_handler(DomainError, unified_exception_handler)

    # 2. Валидационные ошибки
    app.add_exception_handler(
        RequestValidationError, unified_exception_handler
    )

    # 3. HTTP ошибки
    app.add_exception_handler(
        StarletteHTTPException, unified_exception_handler
    )

    # 4. Общий обработчик (самый общий - должен быть последним)
    app.add_exception_handler(Exception, unified_exception_handler)
