# Используем официальный Python образ
FROM python:3.12-slim as base

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем uv
RUN pip install uv

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы конфигурации зависимостей
COPY pyproject.toml uv.lock ./

# Устанавливаем зависимости
RUN uv sync --frozen --no-cache

# Копируем исходный код
COPY src/ ./src/
COPY alembic.ini ./
COPY migrations/ ./migrations/
COPY config/ ./config/

# Создаем пользователя для безопасности
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app
USER app

# Экспонируем порт
EXPOSE 8000

# Устанавливаем переменные окружения
ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Команда для запуска приложения
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
