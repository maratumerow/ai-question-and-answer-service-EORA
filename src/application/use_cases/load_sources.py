import logging
from datetime import UTC, datetime

from src.application.dto.converters import ResponseConverter
from src.application.dto.responses import LoadSourcesResponse
from src.domain.entities import Source
from src.domain.repositories import SourceRepositoryInterface
from src.domain.services import ContentParsingServiceInterface

logger = logging.getLogger(__name__)


class LoadSourcesUseCase:
    """Use case for loading sources from URLs."""

    def __init__(
        self,
        source_repository: SourceRepositoryInterface,
        content_parsing_service: ContentParsingServiceInterface,
    ):
        self.source_repository = source_repository
        self.content_parsing_service = content_parsing_service

    async def execute(self, urls: list[str]) -> LoadSourcesResponse:
        """Execute the use case and return response DTO."""
        logger.info("Starting with %d URLs", len(urls))
        logger.debug("URLs: %s...", urls[:3])  # Show first 3 URLs

        # Parse sources from URLs
        parsed_sources = await self.content_parsing_service.parse_urls(urls)
        logger.info("Parsed %d sources", len(parsed_sources))

        # Calculate parsing failures
        parsing_failed_count = len(urls) - len(parsed_sources)

        # Save sources to repository
        saved_sources: list[Source] = []
        save_failed_count = 0

        for source in parsed_sources:
            try:
                logger.debug("Upserting source: %s", source.url)

                # Create new source with updated timestamp
                updated_source = Source(
                    id=source.id,
                    url=source.url,
                    title=source.title,
                    content=source.content,
                    created_at=source.created_at,
                    updated_at=datetime.now(UTC),
                )

                saved_source = await self.source_repository.create_or_update(
                    updated_source
                )
                logger.debug("Successfully upserted source %s", source.url)
                saved_sources.append(saved_source)

            except Exception as e:
                logger.error("Error upserting source %s: %s", source.url, e)
                logger.debug("Exception details:", exc_info=True)
                save_failed_count += 1
                continue

        # Total failed count = parsing failures + save failures
        total_failed_count = parsing_failed_count + save_failed_count

        logger.info(
            "Returning %d sources, failed: %d (parsing: %d, saving: %d)",
            len(saved_sources),
            total_failed_count,
            parsing_failed_count,
            save_failed_count,
        )

        # Convert to response DTO
        return LoadSourcesResponse(
            sources=[
                ResponseConverter.source_to_response(source)
                for source in saved_sources
            ],
            loaded_count=len(saved_sources),
            failed_count=total_failed_count,
        )
