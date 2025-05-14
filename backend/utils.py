import faiss
import numpy as np
import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def load_vector_db():
    # Path to FAISS index
    index_path = "data/vector_store.faiss"
    
    # Load the FAISS index from disk
    index = faiss.read_index(index_path)
    
    # Create a function to retrieve chunks based on source
    def get_chunks_by_source(source: str):
        return [chunk for chunk in index.chunks if chunk['source'] == source]
    
    return {
        "index": index,
        "get_chunks_by_source": get_chunks_by_source
    }

def get_embedding(text: str, model: str="text-embedding-ada-002") -> list:
    response = client.embeddings.create(
        input=[text],
        model=model
    )
    return response.data[0].embedding

