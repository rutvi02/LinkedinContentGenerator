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
from openai import OpenAI



client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- Load assets ---
index = faiss.read_index("linkedin_posts_index.faiss")
with open("linkedin_top_texts.pkl", "rb") as f:
    texts = pickle.load(f)

embed_model = SentenceTransformer("all-MiniLM-L6-v2")



# --- Retrieval ---
def retrieve_similar_posts(query, k=3):
    query_embedding = embed_model.encode([query])
    _, indices = index.search(np.array(query_embedding), k)
    return [texts[i] for i in indices[0]]

# --- Feedback Logger ---
def save_feedback(post_text, liked, notes, variant_type):
    feedback = {
        "timestamp": datetime.now().isoformat(),
        "post_text": post_text,
        "liked": liked,
        "notes": notes,
        "variant_type": variant_type
    }

    file_path = "simple_feedback_log.csv"
    file_exists = os.path.isfile(file_path)

    with open(file_path, "a", newline='', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=feedback.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(feedback)


# --- Generator ---


def generate_post_rag(topic, tone, k=3, system_prompt_type="brand-focused", prompt_modifier=""):
    examples = retrieve_similar_posts(topic, k)
    example_block = "\n\n".join([f"{i+1}. {ex}" for i, ex in enumerate(examples)])

    user_prompt = (
        f"You've reviewed several top-performing LinkedIn posts:\n\n"
        f"{example_block}\n\n"
        f"Now write a fresh LinkedIn post on the topic: '{topic}', in a {tone.lower()} tone.\n"
        f"If relevant, weave in popular hashtags like {popular_hashtags}, but only where they feel natural and meaningful.\n"
        f"Similarly, these keywords often appear in successful posts: {popular_keywords}. Use them only if they enhance the message — don't force them.\n"
        f"Keep the post engaging, authentic, and between 100-150 words. Conclude with a compelling call-to-action that fits the context.\n\n"
        f"{prompt_modifier.strip()} \n"
        f"Use the examples above only as inspiration, not templates. Your post should feel fresh and context-aware."
    )

    system_prompt = SYSTEM_PROMPTS.get(system_prompt_type, "")

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.4,
        max_tokens=400
    )

    return response.choices[0].message.content.strip()


def get_brand_prompt_modifier(brand_feedback):
    if len(brand_feedback) < 3:
        return "Try to describe the problems faced by the industry right now and how can FuelGrowth help in such cases."

    # Extract and normalize notes
    positive_notes = brand_feedback[brand_feedback["liked"] == "👍 Yes"]["notes"].dropna().str.lower().tolist()

    # Keyword-based refinement
    if any(keyword in note for note in positive_notes for keyword in ["clear", "clarity", "concise", "to the point"]):
        return "Ensure the messaging is clear, concise, and aligned with the brand identity."

    if any("generic" in note or "vague" in note for note in positive_notes):
        return "Avoid generic statements. Include unique value propositions and tangible impact."

    if any("stats" in note or "data" in note or "numbers" in note for note in positive_notes):
        return "Support your points with relevant data or statistics to increase credibility."

    return "Highlight industry trends, show impact clearly, and maintain a confident, professional tone."


def get_founder_prompt_modifier(founder_feedback):
    if len(founder_feedback) < 3:
        return "Make it sound authentic and visionary — as if the founder is sharing their personal journey."

    # Extract and normalize notes
    positive_notes = founder_feedback[founder_feedback["liked"] == "👍 Yes"]["notes"].dropna().str.lower().tolist()

    # Keyword-based refinement
    if any(keyword in note for note in positive_notes for keyword in ["relatable", "personal", "story", "journey", "real", "honest"]):
        return "Include a personal story or reflection. Make it human and relatable."

    if any("technical" in note or "complex" in note for note in positive_notes):
        return "Simplify technical language and focus more on emotional resonance or lessons learned."

    if any("vision" in note or "inspiration" in note or "aspire" in note for note in positive_notes):
        return "Speak from a place of vision — what you believe, where you're headed, and why it matters."

    return "Tell a story that reflects the founder's mindset. Be honest, humble, and visionary."

