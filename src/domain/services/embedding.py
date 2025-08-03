"""Embedding service interface."""

from abc import ABC, abstractmethod


class EmbeddingServiceInterface(ABC):
    """Interface for embedding generation service."""

    @abstractmethod
    def encode(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for list of texts."""

    @abstractmethod
    def encode_single(self, text: str) -> list[float]:
        """Generate embedding for single text."""
