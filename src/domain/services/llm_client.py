"""LLM client interface."""

from abc import ABC, abstractmethod

from src.domain.entities.llm import LLMMessage, LLMResponse


class LLMClientInterface(ABC):
    """Interface for LLM client operations."""

    @abstractmethod
    async def generate(self, messages: list[LLMMessage]) -> LLMResponse:
        """Generate response from messages."""
