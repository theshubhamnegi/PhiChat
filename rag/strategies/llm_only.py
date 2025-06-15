from rag.llm import query_phi

def run(question, embedder=None, collection=None, request_id=None):
    prompt = f"<|user|>\n{question}\n<|assistant|>\n"
    answer = query_phi(question)
    return [], answer