from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.entities import Question


class QuestionRepositoryInterface(ABC):
    """Abstract repository for managing questions."""

    @abstractmethod
    async def get_by_id(self, question_id: UUID) -> Question | None:
        """Get question by ID."""

    @abstractmethod
    async def create(self, question: Question) -> Question:
        """Create new question."""
