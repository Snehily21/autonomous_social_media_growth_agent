from backend.config import get_llm
from loguru import logger
import json
import re


class ProfileAgent:

    def __init__(self):
        self.llm = get_llm()

    def _extract_json(self, text: str):
        """
        Extract JSON object safely from LLM output
        """

        try:

            # Remove markdown code blocks if present
            text = text.replace("```json", "").replace("```", "")

            # Find JSON object inside text
            json_match = re.search(r"\{.*\}", text, re.DOTALL)

            if json_match:
                return json.loads(json_match.group())

            return None

        except Exception as e:
            logger.warning(f"JSON extraction failed: {e}")
            return None

    def analyze_profile(self, linkedin_text: str = "", twitter_text: str = ""):
        """
        Analyze user social media profile and generate profile intelligence
        """

        try:

            prompt = f"""
You are an expert social media growth strategist.

Analyze the following user profile content.

LinkedIn Content:
{linkedin_text}

Twitter Content:
{twitter_text}

Return a structured JSON analysis with these fields:

writing_style
tone
content_topics
posting_frequency
engagement_patterns

Example output:

{{
"writing_style": "educational",
"tone": "technical and informative",
"content_topics": ["AI", "LLM", "RAG"],
"posting_frequency": "3 posts per week",
"engagement_patterns": "tutorials and technical breakdowns receive higher engagement"
}}

IMPORTANT:
Return ONLY valid JSON.
"""

            response = self.llm.invoke(prompt)

            content = response.content

            result = self._extract_json(content)

            if result is None:

                logger.warning("LLM returned non JSON output, using fallback")

                result = {
                    "writing_style": "educational",
                    "tone": "technical",
                    "content_topics": ["AI", "Machine Learning"],
                    "posting_frequency": "unknown",
                    "engagement_patterns": "technical posts perform well"
                }

            return result

        except Exception as e:

            logger.error(f"Profile analysis failed: {e}")

            return {
                "writing_style": "unknown",
                "tone": "unknown",
                "content_topics": [],
                "posting_frequency": "unknown",
                "engagement_patterns": "unknown"
            }