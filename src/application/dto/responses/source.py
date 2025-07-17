from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class SourceResponse(BaseModel):
    """Response object for source information."""

    id: UUID
    url: str
    title: str
    created_at: datetime
    updated_at: datetime | None = None


class LoadSourcesResponse(BaseModel):
    """Response object for loaded sources."""

    sources: list[SourceResponse]
    loaded_count: int
    failed_count: int
