from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass(frozen=True)
class QuestionAnswer:
    """Represents a Q&A session entry."""

    question_id: UUID
    answer_id: UUID
    session_id: UUID | None = None
    created_at: datetime = field(default_factory=datetime.now)
    id: UUID = field(default_factory=uuid4)
