"""Repository implementations."""

import logging
from dataclasses import asdict
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities import Source
from src.domain.exceptions.repository import SourceRepositoryError
from src.domain.repositories import SourceRepositoryInterface
from src.infrastructure.database.models import SourceModel

logger = logging.getLogger(__name__)


class SourceRepository(SourceRepositoryInterface):
    """SQLAlchemy implementation of SourceRepository."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, source_id: UUID) -> Source | None:
        """Get source by ID."""
        try:
            result = await self.session.execute(
                select(SourceModel).where(SourceModel.id == source_id)
            )
            model = result.scalar_one_or_none()
            return self._model_to_domain(model) if model else None
        except SQLAlchemyError as e:
            logger.error(
                "Database error while getting source by ID %s: %s",
                source_id,
                str(e),
            )
            raise SourceRepositoryError(
                f"Failed to get source by ID: {source_id}",
                original_error=e,
            ) from e
        except Exception as e:
            logger.error(
                "Unexpected error while getting source by ID %s: %s",
                source_id,
                str(e),
            )
            raise SourceRepositoryError(
                f"Unexpected error while getting source by ID: {source_id}",
                original_error=e,
            ) from e

    async def get_by_url(self, url: str) -> Source | None:
        """Get source by URL."""
        try:
            result = await self.session.execute(
                select(SourceModel).where(SourceModel.url == url)
            )
            model = result.scalar_one_or_none()
            return self._model_to_domain(model) if model else None
        except SQLAlchemyError as e:
            logger.error(
                "Database error while getting source by URL %s: %s",
                url,
                str(e),
            )
            raise SourceRepositoryError(
                f"Failed to get source by URL: {url}",
                original_error=e,
            ) from e
        except Exception as e:
            logger.error(
                "Unexpected error while getting source by URL %s: %s",
                url,
                str(e),
            )
            raise SourceRepositoryError(
                f"Unexpected error while getting source by URL: {url}",
                original_error=e,
            ) from e

    async def get_all(self) -> list[Source]:
        """Get all sources."""
        try:
            result = await self.session.execute(select(SourceModel))
            models = result.scalars().all()
            return [self._model_to_domain(model) for model in models]
        except SQLAlchemyError as e:
            logger.error(
                "Database error while getting all sources: %s",
                str(e),
            )
            raise SourceRepositoryError(
                "Failed to get all sources",
                original_error=e,
            ) from e
        except Exception as e:
            logger.error(
                "Unexpected error while getting all sources: %s",
                str(e),
            )
            raise SourceRepositoryError(
                "Unexpected error while getting all sources",
                original_error=e,
            ) from e

    async def create_or_update(self, source: Source) -> Source:
        """Create new source or update existing one."""
        try:
            source_data = asdict(source)
            stmt = insert(SourceModel).values(**source_data)

            # On conflict (URL exists), update the fields
            stmt = stmt.on_conflict_do_update(
                index_elements=["url"],
                set_={
                    "title": stmt.excluded.title,
                    "content": stmt.excluded.content,
                    "updated_at": stmt.excluded.updated_at,
                },
            )

            await self.session.execute(stmt)
            await self.session.commit()

            # Get the created/updated record
            result = await self.session.execute(
                select(SourceModel).where(SourceModel.url == source.url)
            )
            model = result.scalar_one()
            return self._model_to_domain(model)

        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(
                "Database error while creating or updating source %s: %s",
                source.id,
                str(e),
            )
            raise SourceRepositoryError(
                f"Failed to create or update source: {source.id}",
                original_error=e,
            ) from e
        except Exception as e:
            await self.session.rollback()
            logger.error(
                "Unexpected error while creating or updating source %s: %s",
                source.id,
                str(e),
            )
            raise SourceRepositoryError(
                f"Unexpected error while creating or updating source: "
                f"{source.id}",
                original_error=e,
            ) from e

    async def update(self, source: Source) -> Source:
        """Update existing source."""
        try:
            result = await self.session.execute(
                select(SourceModel).where(SourceModel.id == source.id)
            )
            model = result.scalar_one()

            model.url = source.url
            model.title = source.title
            model.content = source.content
            model.updated_at = source.updated_at

            await self.session.commit()
            await self.session.refresh(model)
            return self._model_to_domain(model)
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(
                "Database error while updating source %s: %s",
                source.id,
                str(e),
            )
            raise SourceRepositoryError(
                f"Failed to update source: {source.id}",
                original_error=e,
            ) from e
        except Exception as e:
            await self.session.rollback()
            logger.error(
                "Unexpected error while updating source %s: %s",
                source.id,
                str(e),
            )
            raise SourceRepositoryError(
                f"Unexpected error while updating source: {source.id}",
                original_error=e,
            ) from e

    async def delete(self, source_id: UUID) -> bool:
        """Delete source by ID."""
        try:
            result = await self.session.execute(
                select(SourceModel).where(SourceModel.id == source_id)
            )
            model = result.scalar_one_or_none()
            if model:
                await self.session.delete(model)
                await self.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(
                "Database error while deleting source %s: %s",
                source_id,
                str(e),
            )
            raise SourceRepositoryError(
                f"Failed to delete source: {source_id}",
                original_error=e,
            ) from e
        except Exception as e:
            await self.session.rollback()
            logger.error(
                "Unexpected error while deleting source %s: %s",
                source_id,
                str(e),
            )
            raise SourceRepositoryError(
                f"Unexpected error while deleting source: {source_id}",
                original_error=e,
            ) from e

    @staticmethod
    def _model_to_domain(model: SourceModel) -> Source:
        """Convert database model to domain model."""
        source_data = {
            column.name: getattr(model, column.name)
            for column in model.__table__.columns
        }
        return Source(**source_data)

    @staticmethod
    def _domain_to_model(source: Source) -> SourceModel:
        """Convert domain model to database model."""
        source_data = asdict(source)
        return SourceModel(**source_data)
