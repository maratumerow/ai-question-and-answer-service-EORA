from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.entities import Source


class SourceRepositoryInterface(ABC):
    """Abstract repository for managing sources."""

    @abstractmethod
    async def get_by_id(self, source_id: UUID) -> Source | None:
        """Get source by ID."""

    @abstractmethod
    async def get_by_url(self, url: str) -> Source | None:
        """Get source by URL."""

    @abstractmethod
    async def get_all(self) -> list[Source]:
        """Get all sources."""

    @abstractmethod
    async def create(self, source: Source) -> Source:
        """Create new source."""

    @abstractmethod
    async def create_or_update(self, source: Source) -> Source:
        """Create new source or update existing one."""

    @abstractmethod
    async def update(self, source: Source) -> Source:
        """Update existing source."""

    @abstractmethod
    async def delete(self, source_id: UUID) -> bool:
        """Delete source by ID."""
