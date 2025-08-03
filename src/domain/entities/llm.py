"""LLM domain entities."""

from dataclasses import dataclass
from typing import Any


@dataclass
class LLMMessage:
    """Message for LLM."""

    content: str
    role: str = "user"


@dataclass
class LLMResponse:
    """Response from LLM."""

    content: str
    metadata: dict[str, Any] | None = None
