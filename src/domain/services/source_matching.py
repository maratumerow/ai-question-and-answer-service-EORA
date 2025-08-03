import uuid
from abc import ABC, abstractmethod

from src.domain.entities import Source


class SourceMatchingServiceInterface(ABC):
    """Abstract service for matching sources to questions."""

    @abstractmethod
    async def find_relevant_sources(
        self, question: str, limit: int | None = None
    ) -> list[Source]:
        """Find sources relevant to the question."""

    @abstractmethod
    async def add_source_embeddings(self, source: Source) -> None:
        """Add embeddings for a source."""

    @abstractmethod
    async def remove_source_embeddings(self, source_id: uuid.UUID) -> None:
        """Remove embeddings for a source."""

    @abstractmethod
    async def update_source_embeddings(self, source: Source) -> None:
        """Update embeddings for a source."""
