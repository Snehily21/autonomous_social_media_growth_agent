from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from backend.database.db import Base


# PROFILE ANALYSIS TABLE

class ProfileAnalysis(Base):
    __tablename__ = "profile_analysis"

    id = Column(Integer, primary_key=True, index=True)
    linkedin_url = Column(String, nullable=True)
    twitter_url = Column(String, nullable=True)

    writing_style = Column(String)
    tone = Column(String)
    topics = Column(Text)
    posting_frequency = Column(String)
    engagement_patterns = Column(Text)

    created_at = Column(DateTime(timezone=True), server_default=func.now())


# COMPETITOR ANALYSIS TABLE

class CompetitorAnalysis(Base):
    __tablename__ = "competitor_analysis"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profile_analysis.id"))

    competitors = Column(Text)
    high_engagement_topics = Column(Text)
    content_gaps = Column(Text)
    opportunities = Column(Text)

    created_at = Column(DateTime(timezone=True), server_default=func.now())


# CONTENT CALENDAR TABLE

class ContentCalendar(Base):
    __tablename__ = "content_calendar"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profile_analysis.id"))

    day = Column(Integer)
    platform = Column(String)
    topic = Column(String)
    format = Column(String)
    scheduled_time = Column(String)

    created_at = Column(DateTime(timezone=True), server_default=func.now())


# GENERATED POSTS TABLE

class GeneratedPost(Base):
    __tablename__ = "generated_posts"

    id = Column(Integer, primary_key=True, index=True)
    calendar_id = Column(Integer, ForeignKey("content_calendar.id"))

    post_text = Column(Text)
    hashtags = Column(Text)
    image_prompt = Column(Text)

    status = Column(String, default="pending")

    created_at = Column(DateTime(timezone=True), server_default=func.now())