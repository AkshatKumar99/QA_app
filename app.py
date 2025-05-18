import streamlit as st
from backend.retriever import get_relevant_transcripts
from backend.qa_generator import generate_qa_pairs, generate_qa_from_llm_only

import os
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(page_title="MedPod Q&A", layout="centered")

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    .stButton > button {
        width: 100%;
        font-size: 1.2rem;
        padding: 0.75rem;
        border-radius: 0.5rem;
    }
    .stTextInput > div > input {
        font-size: 1.1rem;
        padding: 0.5rem;
    }
    .st-expander {
        font-size: 1.05rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# App Title
st.title("Podcast Q&A")

# Search Input
topic = st.text_input("🔍 Medical Topic", placeholder="e.g. ACS, alcoholic hepatitis, etc.")

# Toggle: Use podcast content?
use_podcast_sources = st.toggle("Use podcast sources (RAG mode)", value=False)

# If using podcasts, show the filter options
selected_sources = []
if use_podcast_sources:
    selected_sources = st.multiselect(
        "Podcast Sources",
        options = ["CoreIM", "Curbsiders", "The Clinical Problem Solver"],
        default = ["CoreIM", "Curbsiders"]
    )

# Submit button
debug = True
if st.button("Generate Questions"):
    if not topic.strip():
        st.warning("⚠️ Please enter a medical topic.")
    else:
        chunks = False
        with st.spinner("🔎 Thinking..."):
            if use_podcast_sources:
                chunks = get_relevant_transcripts(topic, selected_sources, debugging=debug)
            if not chunks:
                st.warning("❌ No relevant podcast content found. Falling back to using OpenAI only.")
                qa_pairs = generate_qa_from_llm_only(topic=topic, debugging=debug)
            else:
                qa_pairs = generate_qa_pairs(chunks, debugging=debug)
        
        if qa_pairs:
            st.success(f"✅ {len(qa_pairs)} Q&A pairs generated!")    
            for i, pair in enumerate(qa_pairs):
                with st.expander(f"Q{i+1}: {pair[0]}"):
                    st.markdown(f"**Answer:** {pair[1]}")
        else:
            st.error("⚠️ No Q&A could be generated.")