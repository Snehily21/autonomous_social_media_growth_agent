import streamlit as st
import requests



st.set_page_config(
    page_title="Autonomous Social Media Growth Agent",
    layout="wide"
)

st.title("🚀 Autonomous Social Media Growth Agent")

st.write(
    "AI system that analyzes your profile, studies competitors, "
    "creates a content strategy and generates social media posts."
)

API_URL = "https://localhost:8000"


# PROFILE INPUT


st.header("Profile Input")

linkedin_text = st.text_area(
    "LinkedIn Profile Content",
    height=150,
    placeholder="Paste LinkedIn profile text or posts..."
)

twitter_text = st.text_area(
    "Twitter / X Profile Content",
    height=150,
    placeholder="Paste Twitter bio or tweets..."
)


# RUN PIPELINE


if st.button("Generate Content Strategy"):

    if not linkedin_text and not twitter_text:

        st.warning("Please enter profile content")

    else:

        with st.spinner("Running AI pipeline..."):

            response = requests.post(
                f"{API_URL}/run-pipeline",
                json={
                    "linkedin_text": linkedin_text,
                    "twitter_text": twitter_text
                }
            )

            data = response.json()

        if data["status"] == "success":

            st.success("Pipeline completed")

            # PROFILE REPORT
            

            st.header("Profile Intelligence")

            st.json(data["profile_report"])

            
            # COMPETITOR REPORT
            

            st.header("Competitor Insights")

            st.json(data["competitor_report"])

            
            # CONTENT CALENDAR
            

            st.header("Content Calendar")

            calendar = data["calendar"]

            for item in calendar:

                st.write(
                    f"Day {item.get('day')} | "
                    f"{item.get('platform')} | "
                    f"{item.get('topic')}"
                )

            
            # GENERATED POSTS
            

            st.header("Generated Posts")

            posts = data["generated_posts"]

            for post in posts:

                day = post.get("day")
                topic = post.get("topic")
                platform = post.get("platform")

                with st.expander(f"Day {day} - {topic}"):

                    st.subheader("Post Text")

                    st.write(post.get("post_text"))

                    if st.button(f"Rewrite Post {day}"):

                        new_post = requests.post(
                            f"{API_URL}/regenerate-post",
                            json={
                                "topic": topic,
                                "platform": platform
                            }
                        )

                        result = new_post.json()

                        st.success("New version generated")

                        st.write(result["post_text"])

                    st.subheader("Hashtags")

                    st.write(post.get("hashtags"))

                    if st.button(f"New Hashtags {day}"):

                        new_hashtags = requests.post(
                            f"{API_URL}/regenerate-hashtags",
                            json={
                                "topic": topic,
                                "platform": platform
                            }
                        )

                        result = new_hashtags.json()

                        st.success("New hashtags generated")

                        st.write(result["hashtags"])

                    st.subheader("Visual Concept")

                    st.write(post.get("visual_concept"))

        else:

            st.error("Pipeline failed")