import logging
import os

from fastapi import Depends

from src.core.config.llm import LLMConfig
from src.core.config.vector_search import VectorSearchConfig
from src.domain.repositories.source import SourceRepositoryInterface
from src.domain.repositories.vector_search import (
    VectorSearchRepositoryInterface,
)
from src.domain.services.embedding import EmbeddingServiceInterface
from src.domain.services.llm_client import LLMClientInterface
from src.domain.services.prompt_template import PromptTemplateInterface
from src.domain.services.text_chunking import TextChunkingServiceInterface
from src.infrastructure.services import HTTPContentParsingService
from src.infrastructure.services.anthropic_llm_client import AnthropicLLMClient
from src.infrastructure.services.llm import AnthropicLLMService
from src.infrastructure.services.postgresql_vector_source_matching import (
    PostgreSQLVectorSourceMatchingService,
    SourceMatchingConfig,
)
from src.infrastructure.services.russian_prompt_template import (
    RussianPromptTemplate,
)
from src.infrastructure.services.sentence_transformer_embedding import (
    SentenceTransformerEmbeddingService,
)
from src.infrastructure.services.simple_text_chunking import (
    SimpleTextChunkingService,
)
from src.presentation.dependencies.repositories.source import (
    get_source_repository,
)
from src.presentation.dependencies.repositories.vector_search import (
    get_vector_search_repository,
)

logger = logging.getLogger(__name__)


def get_llm_client() -> LLMClientInterface:
    """Get LLM client."""
    logger.debug("Creating Anthropic LLM client")
    config = LLMConfig()
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")

    return AnthropicLLMClient(
        api_key=api_key,
        model=config.model,
        temperature=config.temperature,
        max_tokens=config.max_tokens,
    )


def get_prompt_template() -> PromptTemplateInterface:
    """Get prompt template."""
    logger.debug("Creating Russian prompt template")
    return RussianPromptTemplate()


def get_anthropic_service(
    llm_client: LLMClientInterface = Depends(get_llm_client),
    prompt_template: PromptTemplateInterface = Depends(get_prompt_template),
) -> AnthropicLLMService:
    """Get Anthropic LLM service."""
    logger.debug("Creating Anthropic LLM service")
    return AnthropicLLMService(
        llm_client=llm_client,
        prompt_template=prompt_template,
    )


def get_content_parsing_service() -> HTTPContentParsingService:
    """Get content parsing service."""
    logger.debug("Creating HTTP content parsing service")
    return HTTPContentParsingService()


def get_embedding_service() -> EmbeddingServiceInterface:
    """Get embedding service."""
    logger.debug("Creating sentence transformer embedding service")
    config = VectorSearchConfig()
    return SentenceTransformerEmbeddingService(config.embedding_model)


def get_text_chunking_service() -> TextChunkingServiceInterface:
    """Get text chunking service."""
    logger.debug("Creating simple text chunking service")
    config = VectorSearchConfig()
    return SimpleTextChunkingService(
        chunk_size=config.chunk_size,
        chunk_overlap=config.chunk_overlap,
    )


async def get_source_matching_service(
    source_repository: SourceRepositoryInterface = Depends(
        get_source_repository
    ),
    vector_search_repository: VectorSearchRepositoryInterface = Depends(
        get_vector_search_repository
    ),
    embedding_service: EmbeddingServiceInterface = Depends(
        get_embedding_service
    ),
    text_chunking_service: TextChunkingServiceInterface = Depends(
        get_text_chunking_service
    ),
) -> PostgreSQLVectorSourceMatchingService:
    """Get PostgreSQL vector source matching service."""
    config = VectorSearchConfig()
    matching_config = SourceMatchingConfig(
        similarity_threshold=config.similarity_threshold,
        max_relevant_sources=config.max_relevant_sources,
    )

    logger.debug("Creating PostgreSQL vector source matching service")
    return PostgreSQLVectorSourceMatchingService(
        config=matching_config,
        source_repository=source_repository,
        vector_search_repository=vector_search_repository,
        embedding_service=embedding_service,
        text_chunking_service=text_chunking_service,
    )
