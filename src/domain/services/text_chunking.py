"""Text chunking service interface."""

from abc import ABC, abstractmethod


class TextChunkingServiceInterface(ABC):
    """Interface for text chunking service."""

    @abstractmethod
    def chunk_text(self, text: str) -> list[str]:
        """Split text into chunks for embedding."""
