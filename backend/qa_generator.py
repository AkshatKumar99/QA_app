
def generate_qa_pairs(chunks, debugging=False):
    
    if debugging:
        return _debug_return()
    else:
        return []
    
def generate_qa_from_llm_only(topic, debugging=False):
    
    if debugging:
        return _debug_return()
    else:
        return []
        
def _debug_return():
    return [("Question 1", "Answer 1"), ("Question 2", "Answer 2")]