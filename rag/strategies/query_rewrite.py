import logging
from rag.llm import query_phi

def run(question, embedder, collection, request_id=None):
    rewrite_prompt = f"Rewrite the following resume-related question to be more specific:\n\n'{question}'"
    rewritten = query_phi(rewrite_prompt)
    logging.info(f"[{request_id}] Rewritten Question: {rewritten}")
    
    embedding = embedder.encode([rewritten]).tolist()
    results = collection.query(query_embeddings=embedding, n_results=3)
    top_chunks = results["documents"][0]

    if not top_chunks:
        return [], "No relevant context found."

    context = "\n---\n".join(top_chunks)
    prompt = f"Use the following information to answer the question:\n{context}\n\nQuestion: {question}\nAnswer:"
    answer = query_phi(prompt)
    return top_chunks, answer
