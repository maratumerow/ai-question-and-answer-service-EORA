import logging

from fastapi import Depends

from src.application.use_cases import LoadSourcesUseCase
from src.domain.repositories import SourceRepositoryInterface
from src.domain.services import ContentParsingServiceInterface
from src.presentation.dependencies.repositories import get_source_repository
from src.presentation.dependencies.services import get_content_parsing_service

logger = logging.getLogger(__name__)


def get_load_sources_use_case(
    source_repository: SourceRepositoryInterface = Depends(
        get_source_repository
    ),
    content_parsing_service: ContentParsingServiceInterface = Depends(
        get_content_parsing_service
    ),
) -> LoadSourcesUseCase:
    """Get load sources use case."""
    logger.debug("Creating LoadSourcesUseCase")
    return LoadSourcesUseCase(
        source_repository=source_repository,
        content_parsing_service=content_parsing_service,
    )
