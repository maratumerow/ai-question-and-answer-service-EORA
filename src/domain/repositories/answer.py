from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.entities import Answer


class AnswerRepositoryInterface(ABC):
    """Abstract repository for managing answers."""

    @abstractmethod
    async def get_by_id(self, answer_id: UUID) -> Answer | None:
        """Get answer by ID."""

    @abstractmethod
    async def get_by_question_id(self, question_id: UUID) -> Answer | None:
        """Get answer by question ID."""

    @abstractmethod
    async def create(self, answer: Answer) -> Answer:
        """Create new answer."""
