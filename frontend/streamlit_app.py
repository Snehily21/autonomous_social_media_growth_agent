import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.orchestrator.workflow import run_pipeline
from backend.agents.hashtag_agent import HashtagAgent
from backend.agents.copy_agent import CopyAgent


st.set_page_config(
    page_title="Autonomous Social Media Growth Agent",
    page_icon="🚀",
    layout="wide"
)


st.title("🚀 Autonomous Social Media Growth Agent")

st.write(
    "AI system that analyzes your profile, studies competitors, "
    "creates a content strategy and generates social media posts."
)

st.divider()


st.subheader("Profile Input")

linkedin_input = st.text_area(
    "LinkedIn Profile Content",
    placeholder="Paste LinkedIn profile text or posts...",
    height=200
)

twitter_input = st.text_area(
    "Twitter / X Profile Content",
    placeholder="Paste Twitter bio or tweets...",
    height=200
)

st.divider()


if st.button("Generate Content Strategy", use_container_width=True):

    if not linkedin_input and not twitter_input:

        st.warning("Please provide at least one profile input.")
        st.stop()

    with st.spinner("🤖 AI agents are analyzing your profile..."):

        try:

            result = run_pipeline({

                "linkedin_text": linkedin_input,
                "twitter_text": twitter_input

            })

            st.success("Strategy Generated Successfully!")

            st.divider()

            # PROFILE ANALYSIS

            st.subheader("🧠 Profile Analysis")

            st.json(result["profile_report"])


            st.divider()

            # COMPETITOR ANALYSIS

            st.subheader("📊 Competitor Insights")

            st.json(result["competitor_report"])


            st.divider()

            # CONTENT CALENDAR

            st.subheader("📅 Content Calendar")

            calendar = result["calendar"]

            for item in calendar:

                st.write(
                    f"Day {item['day']} | {item['platform']} | {item['topic']}"
                )


            st.divider()

            # GENERATED POSTS

            st.subheader("📈 AI Generated Posts")

            posts = result["generated_posts"]

            for i, post in enumerate(posts):

                st.markdown(f"### Day {post['day']} — {post['platform']}")

                topic = post["topic"]
                platform = post["platform"]

                st.write("**Topic:**", topic)

                st.write("**Post Text:**", post["post_text"])


                if st.button(f"🔁 Regenerate Post {i}"):

                    new_post = CopyAgent().generate_post(topic, platform, {})

                    post["post_text"] = new_post

                    st.success("Post regenerated!")

                    st.write(new_post)


                st.write("**Hashtags:**", post["hashtags"])


                if st.button(f"🔁 Regenerate Hashtags {i}"):

                    new_tags = HashtagAgent().generate_hashtags(topic, platform)

                    post["hashtags"] = new_tags

                    st.success("Hashtags regenerated!")

                    st.write(new_tags)


                st.write("**Visual Concept:**", post["visual_concept"])

                st.divider()


        except Exception as e:

            st.error("Something went wrong while running the AI pipeline.")

            st.exception(e)