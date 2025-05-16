import streamlit as st
from backend.retriever import get_relevant_transcripts
from backend.qa_generator import generate_qa_pairs

import os
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(page_title="MedPod Q&A", layout="centered")

debugging = True

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
selected_sources = st.multiselect(
    "Podcast Sources",
    options = ["CoreIM", "Curbsiders", "The Clinical Problem Solver"],
    default = ["CoreIM", "Curbsiders"]
)

# Submit button
if st.button("Generate Questions"):
    if not topic.strip():
        st.warning("⚠️ Please enter a medical topic.")
    else:
        with st.spinner("Fetching transcripts and generating Q&A..."):
            chunks = get_relevant_transcripts(topic, selected_sources, debugging)
        if not chunks:
            st.error("❌ No relevant podcast content found.")
        else:
            qa_pairs = generate_qa_pairs(chunks, debugging)
            st.success(f"✅ {len(qa_pairs)} Q&A pairs generated!")
            
            for i, pair in enumerate(qa_pairs):
                with st.expander(f"Q{i+1}: {pair[0][i]}"):
                    st.markdown(f"**Answer:** {pair[1][i]}")