"""LLM service implementation with dependency injection."""

import logging

from src.domain.entities import Source
from src.domain.entities.llm import LLMMessage
from src.domain.exceptions.service import LLMServiceError
from src.domain.services import LLMServiceInterface
from src.domain.services.llm_client import LLMClientInterface
from src.domain.services.prompt_template import PromptTemplateInterface

logger = logging.getLogger(__name__)


class AnthropicLLMService(LLMServiceInterface):
    """Clean Architecture LLM service implementation."""

    def __init__(
        self,
        llm_client: LLMClientInterface,
        prompt_template: PromptTemplateInterface,
    ):
        """Initialize with injected dependencies."""
        self.llm_client = llm_client
        self.prompt_template = prompt_template

    async def generate_answer(self, question: str) -> str:
        """Generate answer based on question only."""
        try:
            prompt = self.prompt_template.create_simple_prompt(question)
            message = LLMMessage(content=prompt)

            response = await self.llm_client.generate([message])
            return response.content

        except LLMServiceError:
            raise
        except Exception as e:
            logger.error("Error generating answer: %s", e)
            raise LLMServiceError(
                "Failed to generate answer", original_error=e
            ) from e

    async def generate_answer_with_sources(
        self, question: str, sources: list[Source]
    ) -> str:
        """Generate answer based on question and relevant sources."""
        try:
            prompt = self.prompt_template.create_context_prompt(
                question, sources
            )
            message = LLMMessage(content=prompt)

            response = await self.llm_client.generate([message])
            return response.content

        except LLMServiceError:
            raise
        except Exception as e:
            logger.error("Error generating answer with sources: %s", e)
            raise LLMServiceError(
                "Failed to generate answer with sources", original_error=e
            ) from e
