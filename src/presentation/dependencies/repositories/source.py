from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.repositories import (
    SourceRepository,
)
from src.presentation.dependencies.database import get_db_session


def get_source_repository(
    db_session: AsyncSession = Depends(get_db_session),
) -> SourceRepository:
    """Get source repository."""
    return SourceRepository(db_session)
