import streamlit as st
from sentence_transformers import SentenceTransformer
import faiss
import pickle
import numpy as np
import openai
import csv
import os
from datetime import datetime
from custom_prompts import SYSTEM_PROMPTS
from variables_based_on_EDA import popular_hashtags, popular_keywords
import pandas as pd
from functions import generate_post_rag, get_brand_prompt_modifier, get_founder_prompt_modifier, retrieve_similar_posts, save_feedback
from openai import OpenAI


# --- Load assets ---
index = faiss.read_index("linkedin_posts_index.faiss")
with open("linkedin_top_texts.pkl", "rb") as f:
    texts = pickle.load(f)

embed_model = SentenceTransformer("all-MiniLM-L6-v2")


# Loading feedback data
feedback_df = pd.read_csv("simple_feedback_log.csv")

# Separate feedback by variant type
brand_feedback = feedback_df[feedback_df["variant_type"] == "brand-focused"]
founder_feedback = feedback_df[feedback_df["variant_type"] == "founder-focused"]

#Initializing the client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


# --- Streamlit UI ---
st.title("📢 LinkedIn Content Creator AI Agent")
st.markdown("Automate and optimize LinkedIn posts with AI-powered retrieval + generation.")

topic = st.text_input("🧠 Enter a topic (e.g., AI for Good):")
tone = st.selectbox("Choose a tone:", ["Professional", "Informative", "Inspirational", "Conversational","Bold", "Reflective", "Story-driven"])
k = st.slider("🔍 How many similar examples to retrieve?", 1, 5, 3)

if st.button("✨ Generate 2 Variations"):

    brand_modifier = get_brand_prompt_modifier(brand_feedback=brand_feedback)
    founder_modifier = get_founder_prompt_modifier(founder_feedback=founder_feedback)

    if topic:
        with st.spinner("Generating 2 post variations..."):
            variant_1 = generate_post_rag(topic, tone, k, system_prompt_type="brand-focused", prompt_modifier=brand_modifier)
            variant_2 = generate_post_rag(topic, tone, k, system_prompt_type="founder-focused", prompt_modifier=founder_modifier)

        st.session_state["variant_1"] = variant_1
        st.session_state["variant_2"] = variant_2
    else:
        st.warning("Please enter a topic to generate posts.")

# Show Variants + Feedback if available
if "variant_1" in st.session_state and "variant_2" in st.session_state:
    # Variant 1
    with st.expander("🔁 Variant 1 (brand-focused)"):
        st.text_area("📝 Generated Post 1", value=st.session_state["variant_1"], height=250, key="text_1")
        liked1 = st.radio("Did you like this post?", ["👍 Yes", "👎 No"], key="like_1")
        notes1 = st.text_area("Leave a comment (optional):", key="note_1")
        if st.button("✅ Submit Feedback for Variant 1"):
            save_feedback(
                post_text=st.session_state["variant_1"],
                liked=liked1,
                notes=notes1,
                variant_type="brand-focused"
            )
            st.success("✅ Feedback for Variant 1 recorded.")

    # Variant 2
    with st.expander("🔁 Variant 2 (founder-focused)"):
        st.text_area("📝 Generated Post 2", value=st.session_state["variant_2"], height=250, key="text_2")
        liked2 = st.radio("Did you like this post?", ["👍 Yes", "👎 No"], key="like_2")
        notes2 = st.text_area("Leave a comment (optional):", key="note_2")
        if st.button("✅ Submit Feedback for Variant 2"):
            save_feedback(
                post_text=st.session_state["variant_2"],
                liked=liked2,
                notes=notes2,
                variant_type="founder-focused"
            )
            st.success("✅ Feedback for Variant 2 recorded.")