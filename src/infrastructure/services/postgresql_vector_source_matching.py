"""PostgreSQL vector source matching service with pgvector."""

import logging
import uuid
from dataclasses import dataclass

from src.domain.entities.source import Source
from src.domain.exceptions.service import SourceMatchingServiceError
from src.domain.repositories.source import SourceRepositoryInterface
from src.domain.repositories.vector_search import (
    VectorSearchRepositoryInterface,
    VectorSearchResult,
)
from src.domain.services.embedding import EmbeddingServiceInterface
from src.domain.services.source_matching import SourceMatchingServiceInterface
from src.domain.services.text_chunking import TextChunkingServiceInterface

logger = logging.getLogger(__name__)


@dataclass
class SourceMatchingConfig:
    """Configuration for source matching."""

    similarity_threshold: float
    max_relevant_sources: int


class PostgreSQLVectorSourceMatchingService(SourceMatchingServiceInterface):
    """Сервис для векторного поиска релевантных источников."""

    def __init__(
        self,
        config: SourceMatchingConfig,
        source_repository: SourceRepositoryInterface,
        vector_search_repository: VectorSearchRepositoryInterface,
        embedding_service: EmbeddingServiceInterface,
        text_chunking_service: TextChunkingServiceInterface,
    ) -> None:
        """Инициализация сервиса."""
        self.config = config
        self.source_repository = source_repository
        self.vector_search_repository = vector_search_repository
        self.embedding_service = embedding_service
        self.text_chunking_service = text_chunking_service

    async def find_relevant_sources(
        self, question: str, limit: int | None = None
    ) -> list[Source]:
        """Поиск релевантных источников по векторному сходству."""
        if limit is None:
            limit = self.config.max_relevant_sources

        try:
            logger.info("Looking for %d relevant sources", limit)

            # Генерируем эмбеддинг для запроса
            query_vector = self.embedding_service.encode_single(question)

            # Выполняем векторный поиск
            search_results = await (
                self.vector_search_repository.search_similar_vectors(
                    query_vector=query_vector,
                    threshold=self.config.similarity_threshold,
                    limit=limit,
                )
            )

            logger.info(
                "🔍 Found %d sources with similarity >= %.2f",
                len(search_results),
                self.config.similarity_threshold,
            )

            # Получаем полные объекты Source по найденным ID
            return await self._get_sources_from_results(search_results)

        except Exception as e:
            logger.error("Error in source retrieval: %s", e)
            raise SourceMatchingServiceError(
                "Failed to find relevant sources"
            ) from e

    async def add_source_embeddings(self, source: Source) -> None:
        """Добавляет эмбеддинги для источника (заменяет существующие)."""
        try:
            # Сначала удаляем старые эмбеддинги для этого источника
            await self.vector_search_repository.remove_embeddings(source.id)

            # Разбиваем контент на чанки
            chunks = self.text_chunking_service.chunk_text(source.content)

            # Создаем эмбеддинги для каждого чанка
            embeddings = self.embedding_service.encode(chunks)

            # Сохраняем в базу данных
            await self.vector_search_repository.store_embeddings(
                source_id=source.id,
                embeddings=embeddings,
            )

            logger.debug(
                "Successfully created %d embeddings for source: %s",
                len(embeddings),
                source.url,
            )

        except Exception as e:
            logger.error(
                "Failed to add embeddings for source %s: %s",
                source.url,
                e,
            )
            raise SourceMatchingServiceError(
                f"Failed to add embeddings for source {source.url}"
            ) from e

    async def remove_source_embeddings(self, source_id: uuid.UUID) -> None:
        """Удаляет все эмбеддинги для источника."""
        try:
            await self.vector_search_repository.remove_embeddings(source_id)
            logger.debug(
                "Successfully removed embeddings for source: %s", source_id
            )
        except Exception as e:
            logger.error(
                "Failed to remove embeddings for source %s: %s",
                source_id,
                e,
            )
            raise SourceMatchingServiceError(
                f"Failed to remove embeddings for source {source_id}"
            ) from e

    async def update_source_embeddings(self, source: Source) -> None:
        """Обновляет эмбеддинги для источника."""
        await self.add_source_embeddings(source)

    async def _get_sources_from_results(
        self, search_results: list[VectorSearchResult]
    ) -> list[Source]:
        """Получает полные объекты Source по результатам поиска."""
        sources: list[Source] = []
        for result in search_results:
            logger.debug(
                "   Source %s similarity: %.3f",
                result.source_id,
                result.similarity,
            )

            source = await self.source_repository.get_by_id(result.source_id)
            if source:
                sources.append(source)

        return sources
