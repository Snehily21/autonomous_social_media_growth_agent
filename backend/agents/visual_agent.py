from backend.config import get_llm
from loguru import logger


class VisualAgent:

    def __init__(self):
        self.llm = get_llm()

    def generate_visual_concept(self, topic: str, platform: str):
        """
        Generate a visual concept or image prompt for a social media post
        """

        try:

            prompt = f"""
You are a creative visual designer for social media content.

Generate a visual concept for the following post.

Topic:
{topic}

Platform:
{platform}

Instructions:

1. Suggest a visual idea suitable for the platform
2. Prefer infographic or diagram style visuals
3. Make the concept educational and easy to understand
4. Describe the visual clearly

Return only the visual concept description.

Example output:

Infographic showing the architecture of a RAG pipeline with
three blocks: user query → vector database retrieval → LLM response.
"""

            response = self.llm.invoke(prompt)

            return response.content

        except Exception as e:
            logger.error(f"Visual concept generation failed: {e}")
            return "Simple infographic illustrating the concept"