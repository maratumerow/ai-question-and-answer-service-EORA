from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.repositories import (
    AnswerRepository,
)
from src.presentation.dependencies.database import get_db_session


def get_answer_repository(
    db_session: AsyncSession = Depends(get_db_session),
) -> AnswerRepository:
    """Get answer repository."""
    return AnswerRepository(db_session)
