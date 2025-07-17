from pydantic import Field

from .base import BaseConfig


class LLMConfig(BaseConfig):
    """Configuration for LLM service."""

    model: str = Field(
        default="claude-3-haiku-20240307",
        description="LLM model to use for generating answers",
    )
    max_tokens: int = Field(
        default=1000, description="Maximum number of tokens in the response"
    )
    temperature: float = Field(
        default=0.1, description="Temperature for response generation"
    )
