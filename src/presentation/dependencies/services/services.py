import logging
import os

from src.infrastructure.services import (
    AnthropicLLMService,
    HTTPContentParsingService,
    SimpleSourceMatchingService,
)

logger = logging.getLogger(__name__)


def get_anthropic_service() -> AnthropicLLMService:
    """Get Anthropic LLM service."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        logger.error("ANTHROPIC_API_KEY environment variable is required")
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")

    logger.debug("Creating Anthropic LLM service")
    return AnthropicLLMService(api_key)


def get_content_parsing_service() -> HTTPContentParsingService:
    """Get content parsing service."""
    logger.debug("Creating HTTP content parsing service")
    return HTTPContentParsingService()


def get_source_matching_service() -> SimpleSourceMatchingService:
    """Get source matching service."""
    logger.debug("Creating simple source matching service")
    return SimpleSourceMatchingService()
