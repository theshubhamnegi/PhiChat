from sentence_transformers import CrossEncoder
from rag.llm import query_phi

cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def run(question, embedder, collection, request_id=None):
    embedding = embedder.encode([question]).tolist()
    results = collection.query(query_embeddings=embedding, n_results=10)
    retrieved_chunks = results["documents"][0]

    if not retrieved_chunks:
        return [], "No relevant context found."

    scores = cross_encoder.predict([[question, chunk] for chunk in retrieved_chunks])
    top_chunks = [chunk for _, chunk in sorted(zip(scores, retrieved_chunks), reverse=True)[:3]]
    
    context = "\n---\n".join(top_chunks)
    prompt = f"Use the following information to answer the question:\n{context}\n\nQuestion: {question}\nAnswer:"
    answer = query_phi(prompt)
    return top_chunks, answer
