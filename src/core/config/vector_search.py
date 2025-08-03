"""Configuration for vector search and embeddings."""

import os

from pydantic import BaseModel, Field


class VectorSearchConfig(BaseModel):
    """Configuration for vector search settings."""

    # Embedding model settings
    embedding_model: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2",
        description="Model for creating text embeddings",
    )
    embedding_dimension: int = Field(
        default=384,
        description="Dimension of embeddings (384 for all-MiniLM-L6-v2)",
    )

    # Anthropic settings for LLM
    anthropic_api_key: str | None = Field(
        default_factory=lambda: os.getenv("ANTHROPIC_API_KEY"),
        description="Anthropic API key for ChatAnthropic",
    )
    anthropic_model: str = Field(
        default="claude-3-sonnet-20240229",
        description="Anthropic model for chat",
    )

    # PostgreSQL pgvector settings
    use_pgvector: bool = Field(
        default=True, description="Use PostgreSQL with pgvector extension"
    )

    # Search parameters
    max_relevant_sources: int = Field(
        default=5, description="Maximum number of relevant sources to return"
    )
    similarity_threshold: float = Field(
        default=0.3,
        description="Minimum similarity score for relevant sources",
    )
    chunk_size: int = Field(
        default=500, description="Size of text chunks for embeddings"
    )
    chunk_overlap: int = Field(
        default=50, description="Overlap between text chunks"
    )
