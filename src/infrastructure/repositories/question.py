"""Repository implementations."""

import logging
from dataclasses import asdict
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities import Question
from src.domain.exceptions.repository import QuestionRepositoryError
from src.domain.repositories import (
    QuestionRepositoryInterface,
)
from src.infrastructure.database.models import (
    QuestionModel,
)

logger = logging.getLogger(__name__)


class QuestionRepository(QuestionRepositoryInterface):
    """SQLAlchemy implementation of QuestionRepository."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, question_id: UUID) -> Question | None:
        """Get question by ID."""
        try:
            result = await self.session.execute(
                select(QuestionModel).where(QuestionModel.id == question_id)
            )
            model = result.scalar_one_or_none()
            return self._model_to_domain(model) if model else None
        except SQLAlchemyError as e:
            logger.error(
                "Database error while getting question by ID %s: %s",
                question_id,
                str(e),
            )
            raise QuestionRepositoryError(
                f"Failed to get question by ID: {question_id}",
                original_error=e,
            ) from e
        except Exception as e:
            logger.error(
                "Unexpected error while getting question by ID %s: %s",
                question_id,
                str(e),
            )
            raise QuestionRepositoryError(
                f"Unexpected error while getting question by ID: "
                f"{question_id}",
                original_error=e,
            ) from e

    async def create(self, question: Question) -> Question:
        """Create new question."""
        try:
            model = self._domain_to_model(question)
            self.session.add(model)
            await self.session.commit()
            await self.session.refresh(model)
            return self._model_to_domain(model)
        except IntegrityError as e:
            logger.error(
                "Integrity error while creating question %s: %s",
                question.id,
                str(e),
            )
            raise QuestionRepositoryError(
                f"Question with ID {question.id} already exists",
                original_error=e,
            ) from e
        except SQLAlchemyError as e:
            logger.error(
                "Database error while creating question %s: %s",
                question.id,
                str(e),
            )
            raise QuestionRepositoryError(
                f"Failed to create question: {question.id}",
                original_error=e,
            ) from e
        except Exception as e:
            logger.error(
                "Unexpected error while creating question %s: %s",
                question.id,
                str(e),
            )
            raise QuestionRepositoryError(
                f"Unexpected error while creating question: {question.id}",
                original_error=e,
            ) from e

    @staticmethod
    def _model_to_domain(model: QuestionModel) -> Question:
        """Convert database model to domain model."""
        question_data = {
            column.name: getattr(model, column.name)
            for column in model.__table__.columns
        }
        return Question(**question_data)

    @staticmethod
    def _domain_to_model(question: Question) -> QuestionModel:
        """Convert domain model to database model."""
        question_data = asdict(question)
        return QuestionModel(**question_data)
