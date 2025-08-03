"""Sentence transformer embedding service implementation."""

from sentence_transformers import SentenceTransformer

from src.domain.services.embedding import EmbeddingServiceInterface


class SentenceTransformerEmbeddingService(EmbeddingServiceInterface):
    """Sentence transformer implementation of embedding service."""

    def __init__(
        self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    ):
        self.model = SentenceTransformer(model_name)

    def encode(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for list of texts."""
        embeddings = self.model.encode(texts)
        return [embedding.tolist() for embedding in embeddings]

    def encode_single(self, text: str) -> list[float]:
        """Generate embedding for single text."""
        embedding = self.model.encode(text)
        return embedding.tolist()
