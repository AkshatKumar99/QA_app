import os
import faiss
import numpy as np
from dotenv import load_dotenv
from openai.embeddings_utils import get_embedding
from backend.utils import load_vector_db

# Load environment variables (API keys, paths)
load_dotenv()

def get_relevant_transcripts(query: str, selected_sources: list, N:int=5):
    
    # Step 1: Create query embedding
    query_embedding = get_embedding(query, engine="text-embedding-ada-002")
    
    # Step 2: Load pre-existing vector DB (FAISS index)
    vector_db = load_vector_db()
    
    # Step 3: Retrieve relevant podcast chunks from selected sources
    relevant_chunks = []
    for source in selected_sources:
        chunks = vector_db.get_chunks_by_source(source) # Get chunks for selected source
        
        # Step 4L Compute cosine similarity and filter top N results
        similarities = [cosine_similarity(query_embedding, chunk['embedding']) for chunk in chunks]
        top_chunks = sorted(zip(chunks, similarities), key=lambda x:x[1], reverse=True)[:N] # Top N results
        
        relevant_chunks.extend([chunk[0] for chunk in top_chunks])
        
        
    return relevant_chunks

def cosine_similarity(vec1, vec2):
    """Compute cosine similarity between two vectors."""
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

