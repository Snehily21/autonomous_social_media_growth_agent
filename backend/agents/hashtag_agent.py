from backend.config import get_llm
from loguru import logger


class HashtagAgent:

    def __init__(self):
        self.llm = get_llm()

    def generate_hashtags(self, topic: str, platform: str):
        """
        Generate optimized hashtags for a social media post
        """

        try:

            prompt = f"""
You are a social media growth expert.

Generate relevant hashtags for the following post topic.

Topic:
{topic}

Platform:
{platform}

Rules:

LinkedIn:
- 5 to 8 hashtags
- professional and niche focused

X (Twitter):
- 3 to 5 hashtags
- short and trending

Return only hashtags separated by spaces.

Example:
#AI #MachineLearning #LLM #RAG
"""

            response = self.llm.invoke(prompt)

            return response.content

        except Exception as e:
            logger.error(f"Hashtag generation failed: {e}")
            return "#AI #Tech"