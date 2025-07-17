from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass(frozen=True)
class Answer:
    """Represents an answer to a question."""

    text: str
    created_at: datetime
    processing_time_ms: int
    question_id: UUID
    id: UUID = field(default_factory=uuid4)
