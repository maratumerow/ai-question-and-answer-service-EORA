"""PostgreSQL vector search repository implementation."""

import uuid

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.repositories.vector_search import (
    VectorSearchRepositoryInterface,
    VectorSearchResult,
)
from src.infrastructure.database.models.source_embedding import (
    SourceEmbeddingModel,
)


class PostgreSQLVectorSearchRepository(VectorSearchRepositoryInterface):
    """PostgreSQL implementation of vector search repository."""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def search_similar_vectors(
        self,
        query_vector: list[float],
        threshold: float,
        limit: int,
    ) -> list[VectorSearchResult]:
        """Search for similar vectors using PostgreSQL pgvector."""
        search_query = """
        WITH similarity_scores AS (
            SELECT DISTINCT se.source_id,
                (1 - cosine_distance(se.embedding, :query_vector))
                  as similarity
            FROM source_embeddings se
        )
        SELECT source_id, similarity
        FROM similarity_scores
        WHERE similarity >= :threshold
        ORDER BY similarity DESC
        LIMIT :limit
        """

        # Convert list to pgvector format
        query_vector_str = "[" + ",".join(map(str, query_vector)) + "]"

        result = await self.db_session.execute(
            text(search_query),
            {
                "query_vector": query_vector_str,
                "threshold": threshold,
                "limit": limit,
            },
        )

        rows = result.fetchall()
        return [
            VectorSearchResult(source_id=row[0], similarity=row[1])
            for row in rows
        ]

    async def store_embeddings(
        self,
        source_id: uuid.UUID,
        embeddings: list[list[float]],
    ) -> None:
        """Store embeddings for a source."""
        for embedding in embeddings:
            embedding_model = SourceEmbeddingModel(
                id=uuid.uuid4(),
                source_id=source_id,
                embedding=embedding,
            )
            self.db_session.add(embedding_model)

        await self.db_session.commit()

    async def remove_embeddings(self, source_id: uuid.UUID) -> None:
        """Remove all embeddings for a source."""
        delete_query = text(
            "DELETE FROM source_embeddings WHERE source_id = :source_id"
        )
        await self.db_session.execute(
            delete_query, {"source_id": str(source_id)}
        )
        await self.db_session.commit()
