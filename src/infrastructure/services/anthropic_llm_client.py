"""Anthropic LLM client implementation."""

import logging

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage

from src.domain.entities.llm import LLMMessage, LLMResponse
from src.domain.exceptions.service import LLMServiceError
from src.domain.services.llm_client import LLMClientInterface

logger = logging.getLogger(__name__)


class AnthropicLLMClient(LLMClientInterface):
    """Anthropic implementation of LLM client."""

    def __init__(
        self,
        api_key: str,
        model: str = "claude-3-haiku-20240307",
        temperature: float = 0.1,
        max_tokens: int = 1000,
    ):
        """Initialize Anthropic client."""
        if not api_key:
            raise ValueError("API key is required")

        self.model_name = model

        # Initialize with minimal required parameters
        try:
            self.client = ChatAnthropic(
                model=model,
                api_key=api_key
                temperature=temperature,
                max_tokens=max_tokens,
            )
        except Exception:
            # Fallback initialization
            self.client = ChatAnthropic()
            self.client.model = model
            self.client.api_key = api_key
            self.client.temperature = temperature

    async def generate(self, messages: list[LLMMessage]) -> LLMResponse:
        """Generate response from messages."""
        try:
            # Convert to LangChain format
            langchain_messages = [
                HumanMessage(content=msg.content) for msg in messages
            ]

            response = await self.client.ainvoke(langchain_messages)

            # Extract content as string
            content = response.content
            if isinstance(content, list):
                # Handle list response - join text parts
                content = " ".join(
                    item if isinstance(item, str) else str(item)
                    for item in content
                )

            return LLMResponse(
                content=str(content),
                metadata={
                    "model": self.model_name,
                    "usage": getattr(response, "usage_metadata", None),
                },
            )

        except Exception as e:
            logger.error("Anthropic API error: %s", e)
            raise LLMServiceError("Failed to generate response") from e
