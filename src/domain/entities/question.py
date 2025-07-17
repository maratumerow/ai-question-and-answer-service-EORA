from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass(frozen=True)
class Question:
    """Represents a user question."""

    text: str
    created_at: datetime
    id: UUID = field(default_factory=uuid4)
