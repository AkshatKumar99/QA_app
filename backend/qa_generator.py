import streamlit as st
from openai import OpenAI
from pathlib import Path

client = OpenAI(api_key=st.secrets['openai']['api_key'])

def generate_qa_pairs(chunks, debugging=False):
    
    if debugging:
        return _debug_return()
    


def generate_qa_from_llm_only(topic, debugging=False):

    if debugging:
        return _debug_return()
    
    # Load prompt template
    prompt_path = Path('backend/base_prompt.txt') 
    if not prompt_path.exist():
        st.error("Prompt file 'base_prompt.txt' not found.")
        return []
    
    base_prompt = prompt_path.read_text()
    full_prompt = base_prompt.replace("{topic}", topic)
    
    try:
        response = client.chat.completions.create(
            model='gpt-4',
            messages=[{'role': 'user', 'content': full_prompt}],
            temperature=0.7,
        )
    except Exception as e:
        st.error(f'OpenAI API error: {e}')
        return []
    
    return _parse_qa_output(raw_output)
    
def _parse_qa_output(output: str):
    qa_pairs = []
    blocks = output.split("Q")
    for block in blocks[1:]:
        try:
            q_part, a_part = block.split("A", 1)
            question = q_part.strip("1234567890:. \n-")
            answer = a_part.strip("1234567890:. \n-")
            qa_pairs.append((question, answer))
        except ValueError:
            continue
    return qa_pairs
    
def _debug_return():
    return [("Question 1", "Answer 1"), ("Question 2", "Answer 2")]