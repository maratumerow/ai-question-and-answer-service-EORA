"""SQLAlchemy модель для хранения векторных эмбеддингов."""

import uuid
from typing import TYPE_CHECKING

from pgvector.sqlalchemy import Vector  # type: ignore
from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.models.base import BaseModel

if TYPE_CHECKING:
    from src.infrastructure.database.models.source import SourceModel


class SourceEmbeddingModel(BaseModel):
    """Модель для хранения векторных эмбеддингов источников."""

    __tablename__ = "source_embeddings"

    source_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey("sources.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    # Эмбеддинги хранятся как vector(384) в PostgreSQL для pgvector поддержки
    embedding: Mapped[list[float]] = mapped_column(Vector(384), nullable=False)

    # Связь с источником
    source: Mapped["SourceModel"] = relationship(
        "SourceModel", back_populates="embeddings"
    )

    def __repr__(self) -> str:
        """Строковое представление модели."""
        return (
            f"<SourceEmbeddingModel(id={self.id}, source_id={self.source_id})>"
        )
