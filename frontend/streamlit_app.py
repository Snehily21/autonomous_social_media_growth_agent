import streamlit as st

from backend.orchestrator.workflow import run_pipeline


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
                "linkedin_profile": linkedin_input,
                "twitter_profile": twitter_input
            })

            st.success("Strategy Generated Successfully!")

            st.divider()
            st.subheader("📈 AI Generated Posts")

            for post in result:

                st.markdown(f"### Day {post.get('day')} — {post.get('platform')}")
                st.write("**Topic:**", post.get("topic"))
                st.write("**Post Text:**", post.get("post_text"))
                st.write("**Hashtags:**", post.get("hashtags"))
                st.write("**Visual Concept:**", post.get("visual_concept"))

                st.divider()

        except Exception as e:

            st.error("Something went wrong while running the AI pipeline.")
            st.exception(e)