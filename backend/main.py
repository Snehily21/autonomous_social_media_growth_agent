from fastapi import FastAPI
from pydantic import BaseModel
from backend.orchestrator.workflow import build_workflow
from loguru import logger
from backend.agents.hashtag_agent import HashtagAgent
from backend.agents.copy_agent import CopyAgent

# INITIALIZE FASTAPI


app = FastAPI(
    title="Autonomous Social Media Growth Agent",
    description="AI system for automated social media strategy and content generation",
    version="1.0"
)


# BUILD WORKFLOW


workflow = build_workflow()


# REQUEST SCHEMA


class ProfileInput(BaseModel):

    linkedin_text: str
    twitter_text: str



# HEALTH CHECK


@app.get("/")
def home():
    return {"message": "AI Social Media Growth Agent Running"}



# RUN FULL PIPELINE


@app.post("/run-pipeline")
def run_pipeline(data: ProfileInput):

    try:

        result = workflow.invoke({

            "linkedin_text": data.linkedin_text,
            "twitter_text": data.twitter_text

        })

        return {
            "status": "success",
            "profile_report": result["profile_report"],
            "competitor_report": result["competitor_report"],
            "calendar": result["calendar"],
            "generated_posts": result["generated_posts"]
        }

    except Exception as e:

        logger.error(f"Pipeline failed: {e}")

        return {
            "status": "error",
            "message": str(e)
        }
    
    

@app.post("/regenerate-hashtags")
def regenerate_hashtags(data: dict):

    topic = data["topic"]
    platform = data["platform"]

    hashtags = HashtagAgent.generate_hashtags(topic, platform)

    return {"hashtags": hashtags}



@app.post("/regenerate-post")
def regenerate_post(data: dict):

    topic = data["topic"]
    platform = data["platform"]

    post = CopyAgent.generate_post(topic, platform, {})

    return {"post_text": post}