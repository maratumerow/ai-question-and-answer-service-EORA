from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class QuestionResponse(BaseModel):
    """Response object for question information."""

    id: UUID
    text: str
    created_at: datetime
