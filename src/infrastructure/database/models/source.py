"""Database configuration and models."""

from datetime import datetime

from sqlalchemy import (
    DateTime,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class SourceModel(BaseModel):
    """Database model for sources."""

    __tablename__ = "sources"

    url: Mapped[str] = mapped_column(
        String, unique=True, nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )
