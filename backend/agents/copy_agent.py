from backend.config import get_llm
from backend.rag.retriever import Retriever
from loguru import logger


class CopyAgent:

    def __init__(self):
        self.llm = get_llm()
        self.retriever = Retriever()

    def generate_post(self, topic: str, platform: str, profile_report: dict):
        """
        Generate social media post using RAG context
        """

        try:

            # Retrieve contextual insights
            query = f"content strategy for {topic}"
            context = self.retriever.retrieve_context(query)

            prompt = f"""
You are an expert social media content strategist.

User profile information:
{profile_report}

Retrieved context insights:
{context}

Post Topic:
{topic}

Platform:
{platform}

Instructions:

1. Write an engaging post for the platform
2. Use insights from the retrieved context
3. Match the user's writing tone
4. Make the content educational and actionable

Platform rules:

LinkedIn:
- professional tone
- structured explanation
- longer content

X (Twitter):
- concise and engaging
- conversational style
- thread style if needed

Return only the post text.
"""

            response = self.llm.invoke(prompt)

            return response.content

        except Exception as e:

            logger.error(f"RAG post generation failed: {e}")

            return "Error generating post"