from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class AnswerResponse(BaseModel):
    """Response object for answer information."""

    id: UUID
    question_id: UUID
    text: str
    created_at: datetime
    processing_time_ms: int
