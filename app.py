import streamlit as st
from backend.retriever import get_relevant_transcripts
from backend.qa_generator import generate_qa_pairs

import os
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(page_title='Podcast Q&A Generator', layout="wide")

# App Title
st.title("Podcast Q&A Generator for Medical Teaching")

