from backend.config import get_llm
from loguru import logger
import json
import re


class CompetitorAgent:

    def __init__(self):
        self.llm = get_llm()

    def _extract_json(self, text: str):
        """
        Extract JSON safely from LLM output
        """

        try:

            text = text.replace("```json", "").replace("```", "")

            json_match = re.search(r"\{.*\}", text, re.DOTALL)

            if json_match:
                return json.loads(json_match.group())

            return None

        except Exception as e:

            logger.warning(f"JSON extraction failed: {e}")
            return None

    def analyze_competitors(self, profile_report: dict):
        """
        Analyze competitors based on profile intelligence
        """

        try:

            prompt = f"""
You are a social media growth strategist.

Based on the following user profile intelligence:

{profile_report}

Your tasks:

1. Identify 3-5 relevant competitors in the same niche
2. Identify high engagement content topics
3. Detect content gaps
4. Suggest growth opportunities

Return a structured JSON response.

Example output:

{{
"competitors": ["AI Builder", "LLM Expert", "ML Hacker"],
"high_engagement_topics": ["AI tutorials", "LLM breakdowns", "AI agent demos"],
"content_gaps": ["LangGraph tutorials", "RAG system architecture"],
"opportunities": ["Create beginner-friendly AI agent guides", "Share real-world AI projects"]
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
                    "competitors": ["AI Influencer", "ML Engineer"],
                    "high_engagement_topics": ["AI tutorials", "Machine Learning guides"],
                    "content_gaps": ["LangGraph tutorials"],
                    "opportunities": ["Post hands-on AI tutorials"]
                }

            return result

        except Exception as e:

            logger.error(f"Competitor analysis failed: {e}")

            return {
                "competitors": [],
                "high_engagement_topics": [],
                "content_gaps": [],
                "opportunities": []
            }