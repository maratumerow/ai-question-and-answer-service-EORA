"""Vector search repository interface."""

import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class VectorSearchResult:
    """Result of vector search."""

    source_id: uuid.UUID
    similarity: float


class VectorSearchRepositoryInterface(ABC):
    """Interface for vector search operations."""

    @abstractmethod
    async def search_similar_vectors(
        self,
        query_vector: list[float],
        threshold: float,
        limit: int,
    ) -> list[VectorSearchResult]:
        """Search for similar vectors."""

    @abstractmethod
    async def store_embeddings(
        self,
        source_id: uuid.UUID,
        embeddings: list[list[float]],
    ) -> None:
        """Store embeddings for a source."""

    @abstractmethod
    async def remove_embeddings(self, source_id: uuid.UUID) -> None:
        """Remove all embeddings for a source."""
