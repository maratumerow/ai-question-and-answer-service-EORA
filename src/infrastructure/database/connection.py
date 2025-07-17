from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.core.config import get_settings

settings = get_settings()

# Создание асинхронного движка
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=settings.pool_pre_ping,
    pool_recycle=settings.pool_recycle,
)

# Фабрика сессий
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=True,
    autocommit=False,
)
