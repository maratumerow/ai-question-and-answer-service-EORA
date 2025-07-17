import time
from collections.abc import Awaitable, Callable
from typing import Any

from src.core.logging import get_logger


async def logging_middleware(
    request: Any, call_next: Callable[[Any], Awaitable[Any]]
) -> Any:
    """Middleware для логирования HTTP запросов."""
    logger = get_logger("api.middleware")

    # Логируем входящий запрос
    logger.info(
        "Incoming request: %s %s from %s",
        request.method,
        request.url.path,
        request.client.host if request.client else "unknown",
    )

    start_time = time.time()
    # Выполняем запрос
    response = await call_next(request)

    # Логируем ответ
    process_time = time.time() - start_time
    logger.info(
        "Request completed: %s %s - Status: %d - Time: %.3fs",
        request.method,
        request.url.path,
        response.status_code,
        process_time,
    )

    return response
