from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.repositories import (
    QuestionRepository,
)
from src.presentation.dependencies.database import get_db_session


def get_question_repository(
    db_session: AsyncSession = Depends(get_db_session),
) -> QuestionRepository:
    """Get question repository."""
    return QuestionRepository(db_session)
