"""Prompt template interface."""

from abc import ABC, abstractmethod

from src.domain.entities import Source


class PromptTemplateInterface(ABC):
    """Interface for prompt template operations."""

    @abstractmethod
    def create_simple_prompt(self, question: str) -> str:
        """Create simple prompt for question only."""

    @abstractmethod
    def create_context_prompt(
        self, question: str, sources: list[Source]
    ) -> str:
        """Create prompt with context from sources."""
