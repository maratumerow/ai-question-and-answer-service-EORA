"""Database configuration and models."""

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel

if TYPE_CHECKING:
    from src.infrastructure.database.models.question import QuestionModel


class AnswerModel(BaseModel):
    """Database model for answers."""

    __tablename__ = "answers"

    question_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("questions.id"), nullable=False
    )
    text: Mapped[str] = mapped_column(Text, nullable=False)
    processing_time_ms: Mapped[int] = mapped_column(Integer, nullable=False)

    # Отношения
    question: Mapped["QuestionModel"] = relationship(back_populates="answers")
