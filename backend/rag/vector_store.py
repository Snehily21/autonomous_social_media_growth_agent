import faiss
import numpy as np
import os
import pickle
from loguru import logger

from backend.rag.embeddings import EmbeddingService
from backend.config import VECTOR_DB_PATH


class VectorStore:

    def __init__(self):

        self.embedder = EmbeddingService()

        self.index = None
        self.documents = []

        os.makedirs(VECTOR_DB_PATH, exist_ok=True)

        self.index_file = os.path.join(VECTOR_DB_PATH, "faiss.index")
        self.doc_file = os.path.join(VECTOR_DB_PATH, "documents.pkl")

        self._load_or_create_index()

    def _load_or_create_index(self):

        try:

            if os.path.exists(self.index_file):

                self.index = faiss.read_index(self.index_file)

                with open(self.doc_file, "rb") as f:
                    self.documents = pickle.load(f)

                logger.info("Loaded existing vector store")

            else:

                # default embedding dimension
                dimension = 384

                self.index = faiss.IndexFlatL2(dimension)

                logger.info("Created new FAISS index")

        except Exception as e:

            logger.error(f"Vector store initialization failed: {e}")
            raise

    def add_documents(self, docs: list):

        try:

            embeddings = self.embedder.embed_documents(docs)

            vectors = np.array(embeddings).astype("float32")

            self.index.add(vectors)

            self.documents.extend(docs)

            self._save()

            logger.info("Documents added to vector store")

        except Exception as e:

            logger.error(f"Adding documents failed: {e}")

    def search(self, query: str, k: int = 3):

        try:

        # If no documents stored yet
            if len(self.documents) == 0:
                logger.warning("Vector store empty, skipping search")
                return []

            query_embedding = self.embedder.embed_text(query)

            vector = np.array([query_embedding]).astype("float32")

            distances, indices = self.index.search(vector, k)

            results = []

            for idx in indices[0]:

                if idx >= 0 and idx < len(self.documents):
                    results.append(self.documents[idx])

            return results

        except Exception as e:

            logger.error(f"Vector search failed: {e}")

            return []
    

    def _save(self):

        try:

            faiss.write_index(self.index, self.index_file)

            with open(self.doc_file, "wb") as f:
                pickle.dump(self.documents, f)

        except Exception as e:

            logger.error(f"Saving vector store failed: {e}")