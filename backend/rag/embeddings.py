from backend.config import get_embedding_model
from loguru import logger


class EmbeddingService:

    def __init__(self):
        """
        Load embedding model once
        """
        try:
            self.model = get_embedding_model()
            logger.info("Embedding model loaded successfully")

        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")
            raise

    def embed_text(self, text: str):
        """
        Convert a single text into embedding vector
        """

        try:

            embedding = self.model.encode(text)

            return embedding.tolist()

        except Exception as e:

            logger.error(f"Embedding generation failed: {e}")

            return None

    def embed_documents(self, documents: list):
        """
        Convert multiple documents into embeddings
        """

        try:

            embeddings = self.model.encode(documents)

            return embeddings.tolist()

        except Exception as e:

            logger.error(f"Document embedding failed: {e}")

            return []