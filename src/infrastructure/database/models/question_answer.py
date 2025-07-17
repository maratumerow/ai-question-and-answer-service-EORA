"""Database configuration and models."""

import uuid

from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel


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


class QuestionModel(BaseModel):
    """Database model for questions."""

    __tablename__ = "questions"

    text: Mapped[str] = mapped_column(Text, nullable=False)

    # Отношения - используем форвард-ссылку для избежания циклического импорта
    answers: Mapped[list[AnswerModel]] = relationship(
        back_populates="question"
    )
