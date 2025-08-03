import logging
from dataclasses import dataclass
from datetime import UTC, datetime

from src.application.dto.converters import ResponseConverter
from src.application.dto.responses import LoadSourcesResponse
from src.domain.entities import Source
from src.domain.repositories import SourceRepositoryInterface
from src.domain.services import ContentParsingServiceInterface
from src.domain.services.source_matching import SourceMatchingServiceInterface

logger = logging.getLogger(__name__)


@dataclass
class LoadResult:
    """Result of loading a single source."""

    source: Source | None
    success: bool
    error: str | None = None


@dataclass
class LoadSummary:
    """Summary of the entire load operation."""

    loaded_sources: list[Source]
    parsing_failed_count: int
    saving_failed_count: int
    embedding_failed_count: int

    @property
    def total_failed_count(self) -> int:
        return self.parsing_failed_count + self.saving_failed_count


class LoadSourcesUseCase:
    """Use case for loading sources from URLs."""

    def __init__(
        self,
        source_repository: SourceRepositoryInterface,
        content_parsing_service: ContentParsingServiceInterface,
        source_matching_service: SourceMatchingServiceInterface,
    ):
        self.source_repository = source_repository
        self.content_parsing_service = content_parsing_service
        self.source_matching_service = source_matching_service

    async def execute(self, urls: list[str]) -> LoadSourcesResponse:
        """Execute the use case and return response DTO."""
        logger.info("Starting load operation with %d URLs", len(urls))

        # Step 1: Parse sources from URLs
        summary = await self._load_sources_from_urls(urls)

        # Step 2: Convert to response DTO
        return self._create_response(summary)

    async def _load_sources_from_urls(self, urls: list[str]) -> LoadSummary:
        """Load sources from URLs and return summary."""
        # Parse sources from URLs
        parsed_sources = await self.content_parsing_service.parse_urls(urls)
        parsing_failed_count = len(urls) - len(parsed_sources)

        logger.info(
            "Parsed %d/%d sources successfully", len(parsed_sources), len(urls)
        )

        # Process each source
        load_results: list[LoadResult] = []
        for source in parsed_sources:
            result = await self._process_single_source(source)
            load_results.append(result)

        # Calculate summary
        successful_results: list[LoadResult] = [
            r for r in load_results if r.success and r.source
        ]
        loaded_sources = [r.source for r in successful_results if r.source]
        saving_failed_count = len([r for r in load_results if not r.success])
        embedding_failed_count = 0  # Count separately if needed

        return LoadSummary(
            loaded_sources=loaded_sources,
            parsing_failed_count=parsing_failed_count,
            saving_failed_count=saving_failed_count,
            embedding_failed_count=embedding_failed_count,
        )

    async def _process_single_source(self, source: Source) -> LoadResult:
        """Process a single source: save and create embeddings."""
        try:
            # Update timestamp and save
            updated_source = self._prepare_source_for_save(source)
            saved_source = await self.source_repository.create_or_update(
                updated_source
            )

            logger.debug("Successfully saved source: %s", source.url)

            # Create embeddings (non-blocking failure)
            await self._create_embeddings_safely(saved_source)

            return LoadResult(source=saved_source, success=True)

        except Exception as e:
            logger.error("Failed to process source %s: %s", source.url, e)
            return LoadResult(source=None, success=False, error=str(e))

    def _prepare_source_for_save(self, source: Source) -> Source:
        """Prepare source for saving with updated timestamp."""
        return Source(
            id=source.id,
            url=source.url,
            title=source.title,
            content=source.content,
            created_at=source.created_at,
            updated_at=datetime.now(UTC),
        )

    async def _create_embeddings_safely(self, source: Source) -> None:
        """Create embeddings with error handling."""
        try:
            logger.debug("Creating embeddings for source: %s", source.url)
            await self.source_matching_service.add_source_embeddings(source)
            logger.debug("Successfully created embeddings for: %s", source.url)
        except Exception as e:
            logger.warning(
                "Failed to create embeddings for %s: %s", source.url, e
            )
            # Note: We don't re-raise here to allow the main process
            # to continue

    def _create_response(self, summary: LoadSummary) -> LoadSourcesResponse:
        """Create response DTO from summary."""
        logger.info(
            "Load operation completed: %d loaded, %d failed "
            "(parsing: %d, saving: %d)",
            len(summary.loaded_sources),
            summary.total_failed_count,
            summary.parsing_failed_count,
            summary.saving_failed_count,
        )

        return LoadSourcesResponse(
            sources=[
                ResponseConverter.source_to_response(source)
                for source in summary.loaded_sources
            ],
            loaded_count=len(summary.loaded_sources),
            failed_count=summary.total_failed_count,
        )
