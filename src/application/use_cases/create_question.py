import uuid
from datetime import UTC, datetime

from src.domain.entities import Question
from src.domain.repositories import QuestionRepositoryInterface


class CreateQuestionUseCase:
    """Use case for creating questions."""

    def __init__(self, question_repository: QuestionRepositoryInterface):
        self.question_repository = question_repository

    async def execute(self, question_text: str) -> Question:
        """Create and save a new question."""
        question = Question(
            id=uuid.uuid4(),
            text=question_text,
            created_at=datetime.now(UTC),
        )

        return await self.question_repository.create(question)
