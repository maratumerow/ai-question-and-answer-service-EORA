"""Database configuration and models."""

from typing import TYPE_CHECKING

from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel

if TYPE_CHECKING:
    from src.infrastructure.database.models.answer import AnswerModel


class QuestionModel(BaseModel):
    """Database model for questions."""

    __tablename__ = "questions"

    text: Mapped[str] = mapped_column(Text, nullable=False)

    # Отношения - используем форвард-ссылку для избежания циклического импорта
    answers: Mapped[list["AnswerModel"]] = relationship(
        back_populates="question"
    )
