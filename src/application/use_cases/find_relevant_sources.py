from src.domain.entities import Source
from src.domain.services import SourceMatchingServiceInterface


class FindRelevantSourcesUseCase:
    """Use case for finding relevant sources for a question."""

    def __init__(
        self,
        source_matching_service: SourceMatchingServiceInterface,
    ):
        self.source_matching_service = source_matching_service

    async def execute(self, question_text: str) -> list[Source]:
        """Find relevant sources for a question."""
        # Get all sources from the database

        # Find relevant sources using matching service
        return await self.source_matching_service.find_relevant_sources(
            question_text
        )
