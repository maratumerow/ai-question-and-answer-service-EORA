from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass(frozen=True)
class Source:
    """Represents a source of information."""

    url: str
    title: str
    content: str
    created_at: datetime
    updated_at: datetime | None = None
    id: UUID = field(default_factory=uuid4)
