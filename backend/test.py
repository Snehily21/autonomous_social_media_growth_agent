
from agents.profile_agent import ProfileAgent
from agents.competitor_agent import CompetitorAgent
from agents.calendar_agent import CalendarAgent
from agents.copy_agent import CopyAgent
from agents.hashtag_agent import HashtagAgent
from agents.visual_agent import VisualAgent
from orchestrator.workflow import build_workflow

workflow=build_workflow()
result=workflow.invoke({
    "linkedin_text":"Experienced software engineer with a passion for AI and machine learning. Skilled in Python, Java, and cloud technologies. Proven track record of delivering high-quality software solutions and driving innovation in fast-paced environments.",
    "twitter_text":"Tech enthusiast sharing insights on AI, machine learning, and software development. Following the latest trends in technology and providing tips for developers. #AI #MachineLearning #SoftwareDevelopment",
})
print(result["generated_posts"])

"""
agent=VisualAgent()
profile_report={
    "writing_style": "educational",
    "tone": "technical and informative",
    "content_type": ["AI", "LLM", "RAG"],
    "posting_frequency": "3 posts per week",
    "engagement_patterns": "tutorials and technical breakdowns receive higher engagement"
}
competitor_report={
    "competitors": ["AI Builder", "LLM Expert", "ML Hacker"],
    "high_engagement_topics": ["AI tutorials", "LLM breakdowns", "AI agent demos"],
    "content_gaps": ["LangGraph tutorials", "RAG system architecture"],
    "opportunities": ["Create beginner-friendly AI agent guides", "Share real-world AI projects"]
}


result=agent.generate_visual_concept(topic="AI agents explained", platform="X")
print(result)
llm=get_llm()
response = llm.invoke("What is the capital of France?")
print(response.content)

print(engine)
agent=ProfileAgent()
result=agent.analyze_profile(linkedin_text="Experienced software engineer with a passion for AI and machine learning. Skilled in Python, Java, and cloud technologies. Proven track record of delivering high-quality software solutions and driving innovation in fast-paced environments.", twitter_text="Tech enthusiast sharing insights on AI, machine learning, and software development. Following the latest trends in technology and providing tips for developers. #AI #MachineLearning #SoftwareDevelopment")
print(result)"""


