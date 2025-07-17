from abc import ABC, abstractmethod

from src.domain.entities import Source


class SourceMatchingServiceInterface(ABC):
    """Abstract service for matching sources to questions."""

    @abstractmethod
    async def find_relevant_sources(
        self, question: str, sources: list[Source]
    ) -> list[Source]:
        """Find sources relevant to the question."""
