from abc import ABC, abstractmethod

from src.domain.entities import Source


class ContentParsingServiceInterface(ABC):
    """Abstract service for content parsing."""

    @abstractmethod
    async def parse_url(self, url: str) -> Source | None:
        """Parse content from URL."""

    @abstractmethod
    async def parse_urls(self, urls: list[str]) -> list[Source]:
        """Parse content from multiple URLs."""
