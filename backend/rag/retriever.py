from backend.rag.vector_store import VectorStore
from loguru import logger


class Retriever:

    def __init__(self):

        self.vector_store = VectorStore()

    def retrieve_context(self, query: str, top_k: int = 3):
        """
        Retrieve relevant documents from vector DB
        """

        try:

            results = self.vector_store.search(query, k=top_k)

            context = "\n".join(results)

            return context

        except Exception as e:

            logger.error(f"Context retrieval failed: {e}")

            return ""

    def store_analysis_reports(self, profile_report: dict, competitor_report: dict):
        """
        Store analysis reports in vector DB for RAG
        """

        try:

            docs = []

            for key, value in profile_report.items():

                docs.append(f"Profile insight: {key} - {value}")

            for key, value in competitor_report.items():

                docs.append(f"Competitor insight: {key} - {value}")

            self.vector_store.add_documents(docs)

            logger.info("Analysis reports stored in vector DB")

        except Exception as e:

            logger.error(f"Failed to store analysis reports: {e}")