"""Service implementations with safe text extraction."""

import logging

from anthropic import AsyncAnthropic
from anthropic.types import Message

from src.core.config.llm import LLMConfig
from src.domain.entities import Source
from src.domain.exceptions.service import LLMServiceError
from src.domain.services import LLMServiceInterface

from .prompt_builder import PromptBuilder

logger = logging.getLogger(__name__)


class AnthropicLLMService(LLMServiceInterface):
    """Anthropic Claude implementation of LLMService."""

    def __init__(self, api_key: str):
        self.client = AsyncAnthropic(api_key=api_key)
        self.config = LLMConfig()
        self.prompt_builder = PromptBuilder()

    async def generate_answer(self, question: str) -> str:
        """Generate answer based on question only."""
        try:
            if not question or not question.strip():
                raise LLMServiceError("Question cannot be empty")

            prompt = f"Пожалуйста, ответьте на следующий вопрос: {question}"

            response: Message = await self._call_anthropic_api(prompt)

            return self._extract_text_from_response(response)

        except LLMServiceError:
            raise
        except Exception as e:
            logger.error("Error generating answer: %s", e)
            raise LLMServiceError(
                "Failed to generate answer", original_error=e
            )

    async def generate_answer_with_sources(
        self, question: str, sources: list[Source]
    ) -> str:
        """Generate answer based on question and relevant sources."""
        try:
            prompt = self.prompt_builder.build_prompt_with_sources(
                question, sources
            )

            response: Message = await self._call_anthropic_api(prompt)

            return self._extract_text_from_response(response)

        except LLMServiceError:
            raise
        except Exception as e:
            logger.error("Error generating answer with sources: %s", e)
            raise LLMServiceError(
                "Failed to generate answer with sources", original_error=e
            )

    async def _call_anthropic_api(self, prompt: str) -> Message:
        """Centralized API call with error handling."""
        try:
            return await self.client.messages.create(
                model=self.config.model,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                messages=[{"role": "user", "content": prompt}],
            )
        except Exception as e:
            logger.error("Error calling Anthropic API: %s", e)
            raise LLMServiceError(
                "Failed to call Anthropic API", original_error=e
            )

    def _extract_text_from_response(self, response: Message) -> str:
        """Extract text from Anthropic response."""
        try:
            for content_block in response.content:
                if hasattr(content_block, "text"):
                    text_value = getattr(content_block, "text", "")
                    return str(text_value) if text_value else ""
            return ""

        except Exception as e:
            logger.error("Error extracting text from response: %s", e)
            raise LLMServiceError(
                "Failed to extract text from LLM response", original_error=e
            )
