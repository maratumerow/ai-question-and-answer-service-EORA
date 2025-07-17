import logging
from dataclasses import asdict
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities import Answer
from src.domain.exceptions.repository import AnswerRepositoryError
from src.domain.repositories import (
    AnswerRepositoryInterface,
)
from src.infrastructure.database.models.question_answer import (
    AnswerModel,
)

logger = logging.getLogger(__name__)


class AnswerRepository(AnswerRepositoryInterface):
    """SQLAlchemy implementation of AnswerRepository."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, answer_id: UUID) -> Answer | None:
        """Get answer by ID."""
        try:
            result = await self.session.execute(
                select(AnswerModel).where(AnswerModel.id == answer_id)
            )
            model = result.scalar_one_or_none()
            return self._model_to_domain(model) if model else None
        except SQLAlchemyError as e:
            logger.error(
                "Database error while getting answer by ID %s: %s",
                answer_id,
                str(e),
            )
            raise AnswerRepositoryError(
                f"Failed to get answer by ID: {answer_id}", original_error=e
            ) from e
        except Exception as e:
            logger.error(
                "Unexpected error while getting answer by ID %s: %s",
                answer_id,
                str(e),
            )
            raise AnswerRepositoryError(
                f"Unexpected error while getting answer by ID: {answer_id}",
                original_error=e,
            ) from e

    async def get_by_question_id(self, question_id: UUID) -> Answer | None:
        """Get answer by question ID."""
        try:
            result = await self.session.execute(
                select(AnswerModel).where(
                    AnswerModel.question_id == question_id
                )
            )
            model = result.scalar_one_or_none()
            return self._model_to_domain(model) if model else None
        except SQLAlchemyError as e:
            logger.error(
                "Database error while getting answer by question ID %s: %s",
                question_id,
                str(e),
            )
            raise AnswerRepositoryError(
                f"Failed to get answer by question ID: {question_id}",
                original_error=e,
            ) from e
        except Exception as e:
            logger.error(
                "Unexpected error while getting answer by question ID %s: %s",
                question_id,
                str(e),
            )
            raise AnswerRepositoryError(
                "Unexpected error while getting answer by question ID: "
                f"{question_id}",
                original_error=e,
            ) from e

    async def create(self, answer: Answer) -> Answer:
        """Create new answer."""
        try:
            model = self._domain_to_model(answer)
            self.session.add(model)
            await self.session.commit()
            await self.session.refresh(model)
            return self._model_to_domain(model)
        except AnswerRepositoryError:
            # Пробросить доменные исключения без изменений
            raise
        except IntegrityError as e:
            logger.error(
                "Integrity error while creating answer %s: %s",
                answer.id,
                str(e),
            )
            raise AnswerRepositoryError(
                f"Answer with ID {answer.id} "
                "already exists or violates constraints",
                original_error=e,
            ) from e
        except SQLAlchemyError as e:
            logger.error(
                "Database error while creating answer %s: %s",
                answer.id,
                str(e),
            )
            raise AnswerRepositoryError(
                f"Failed to create answer: {answer.id}", original_error=e
            ) from e
        except Exception as e:
            logger.error(
                "Unexpected error while creating answer %s: %s",
                answer.id,
                str(e),
            )
            raise AnswerRepositoryError(
                f"Unexpected error while creating answer: {answer.id}",
                original_error=e,
            ) from e

    @staticmethod
    def _model_to_domain(model: AnswerModel) -> Answer:
        """Convert database model to domain model."""
        answer_data = {
            column.name: getattr(model, column.name)
            for column in model.__table__.columns
        }
        return Answer(**answer_data)

    @staticmethod
    def _domain_to_model(answer: Answer) -> AnswerModel:
        """Convert domain model to database model."""
        answer_data = asdict(answer)
        return AnswerModel(**answer_data)
