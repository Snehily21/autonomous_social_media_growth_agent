from langgraph.graph import StateGraph, END
from typing import TypedDict, List

from backend.rag.retriever import Retriever
from backend.agents.profile_agent import ProfileAgent
from backend.agents.competitor_agent import CompetitorAgent
from backend.agents.calendar_agent import CalendarAgent
from backend.agents.copy_agent import CopyAgent
from backend.agents.hashtag_agent import HashtagAgent
from backend.agents.visual_agent import VisualAgent


# STATE STRUCTURE

class AgentState(TypedDict):

    linkedin_text: str
    twitter_text: str

    profile_report: dict
    competitor_report: dict
    calendar: List

    generated_posts: List


# INITIALIZE AGENTS

retriever = Retriever()

profile_agent = ProfileAgent()
competitor_agent = CompetitorAgent()
calendar_agent = CalendarAgent()

copy_agent = CopyAgent()
hashtag_agent = HashtagAgent()
visual_agent = VisualAgent()


# PROFILE ANALYSIS

def run_profile_analysis(state: AgentState):

    result = profile_agent.analyze_profile(
        linkedin_text=state["linkedin_text"],
        twitter_text=state["twitter_text"]
    )

    state["profile_report"] = result

    return state


# COMPETITOR ANALYSIS

def run_competitor_analysis(state: AgentState):

    result = competitor_agent.analyze_competitors(
        profile_report=state["profile_report"]
    )

    state["competitor_report"] = result

    retriever.store_analysis_reports(
        state["profile_report"],
        state["competitor_report"]
    )

    return state


# CALENDAR GENERATION

def run_calendar_generation(state: AgentState):

    result = calendar_agent.generate_calendar(
        profile_report=state["profile_report"],
        competitor_report=state["competitor_report"],
        days=5
    )

    state["calendar"] = result

    return state


# CONTENT GENERATION

def run_content_generation(state: AgentState):

    calendar = state["calendar"]
    profile = state["profile_report"]

    generated_posts = []

    for item in calendar:

        topic = item.get("topic")
        platform = item.get("platform")

        post_text = copy_agent.generate_post(topic, platform, profile)

        hashtags = hashtag_agent.generate_hashtags(topic, platform)

        visual = visual_agent.generate_visual_concept(topic, platform)

        generated_posts.append({
            "day": item.get("day"),
            "platform": platform,
            "topic": topic,
            "post_text": post_text,
            "hashtags": hashtags,
            "visual_concept": visual
        })

    state["generated_posts"] = generated_posts

    return state


# BUILD GRAPH

def build_workflow():

    graph = StateGraph(AgentState)

    graph.add_node("profile_analysis", run_profile_analysis)
    graph.add_node("competitor_analysis", run_competitor_analysis)
    graph.add_node("calendar_generation", run_calendar_generation)
    graph.add_node("content_generation", run_content_generation)

    graph.set_entry_point("profile_analysis")

    graph.add_edge("profile_analysis", "competitor_analysis")
    graph.add_edge("competitor_analysis", "calendar_generation")
    graph.add_edge("calendar_generation", "content_generation")
    graph.add_edge("content_generation", END)

    workflow = graph.compile()

    return workflow


# PIPELINE RUN FUNCTION

workflow = build_workflow()


def run_pipeline(data):

    result = workflow.invoke({

        "linkedin_text": data["linkedin_text"],
        "twitter_text": data["twitter_text"]

    })

    return result