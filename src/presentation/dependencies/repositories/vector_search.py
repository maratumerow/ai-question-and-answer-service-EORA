"""Vector search repository dependencies."""

import logging

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.repositories.vector_search import (
    VectorSearchRepositoryInterface,
)
from src.infrastructure.repositories.postgresql_vector_search import (
    PostgreSQLVectorSearchRepository,
)
from src.presentation.dependencies.database import get_db_session

logger = logging.getLogger(__name__)


async def get_vector_search_repository(
    db_session: AsyncSession = Depends(get_db_session),
) -> VectorSearchRepositoryInterface:
    """Get PostgreSQL vector search repository."""
    logger.debug("Creating PostgreSQL vector search repository")
    return PostgreSQLVectorSearchRepository(db_session)
