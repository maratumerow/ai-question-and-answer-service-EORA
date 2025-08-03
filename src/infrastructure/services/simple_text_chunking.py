"""Simple text chunking service implementation."""

from src.domain.services.text_chunking import TextChunkingServiceInterface


class SimpleTextChunkingService(TextChunkingServiceInterface):
    """Simple text chunking implementation."""

    def __init__(self, chunk_size: int = 200, chunk_overlap: int = 20):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_text(self, text: str) -> list[str]:
        """Split text into chunks."""
        if not text.strip():
            return []

        words = text.split()
        if len(words) <= self.chunk_size:
            return [text.strip()]

        chunks: list[str] = []
        for i in range(0, len(words), self.chunk_size - self.chunk_overlap):
            start = max(0, i)
            end = min(len(words), i + self.chunk_size)

            chunk = " ".join(words[start:end])
            if chunk.strip():
                chunks.append(chunk.strip())

            # Break if we've reached the end
            if end >= len(words):
                break

        return chunks
