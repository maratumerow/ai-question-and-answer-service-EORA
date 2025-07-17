from abc import ABC, abstractmethod

from src.domain.entities import Source


class LLMServiceInterface(ABC):
    """Abstract service for LLM interactions."""

    @abstractmethod
    async def generate_answer(self, question: str) -> str:
        """Generate answer based on question."""

    @abstractmethod
    async def generate_answer_with_sources(
        self, question: str, sources: list[Source]
    ) -> str:
        """Generate answer based on question and relevant sources."""
