from backend.config import get_llm
from loguru import logger
import json
import re


class CalendarAgent:

    def __init__(self):
        self.llm = get_llm()

    def _extract_json(self, text: str):
        """
        Extract JSON array safely from LLM output
        """

        try:

            text = text.replace("```json", "").replace("```", "")

            json_match = re.search(r"\[.*\]", text, re.DOTALL)

            if json_match:
                return json.loads(json_match.group())

            return None

        except Exception as e:

            logger.warning(f"Calendar JSON extraction failed: {e}")
            return None

    def generate_calendar(self, profile_report: dict, competitor_report: dict, days: int = 14):
        """
        Generate a structured content calendar
        """

        try:

            prompt = f"""
You are a social media strategy expert.

User Profile Insights:
{profile_report}

Competitor Insights:
{competitor_report}

Generate a {days}-day content calendar.

Each item must contain:

day
platform
topic
content_format
posting_time

Platforms allowed:
LinkedIn
X

Content formats:
Post
Thread
Carousel
Article
Poll

Return ONLY a JSON array.

Example:

[
 {{
  "day": 1,
  "platform": "LinkedIn",
  "topic": "Beginner guide to RAG",
  "content_format": "Carousel",
  "posting_time": "10:00 AM"
 }},
 {{
  "day": 2,
  "platform": "X",
  "topic": "AI agents explained",
  "content_format": "Thread",
  "posting_time": "7:00 PM"
 }}
]
"""

            response = self.llm.invoke(prompt)

            content = response.content

            calendar = self._extract_json(content)

            if calendar is None or not isinstance(calendar, list):

                logger.warning("Calendar agent returned non JSON output, using fallback")

                calendar = [
                    {
                        "day": 1,
                        "platform": "LinkedIn",
                        "topic": "Introduction to AI agents",
                        "content_format": "Post",
                        "posting_time": "10:00 AM"
                    },
                    {
                        "day": 2,
                        "platform": "X",
                        "topic": "What is RAG in AI systems?",
                        "content_format": "Thread",
                        "posting_time": "7:00 PM"
                    }
                ]

            return calendar

        except Exception as e:

            logger.error(f"Calendar generation failed: {e}")

            return []