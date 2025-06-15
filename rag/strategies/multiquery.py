from rag.llm import query_phi

def generate_queries(original_query):
    return [
        original_query,
        f"What skills relate to: {original_query}",
        f"What experience matches: {original_query}"
    ]

def run(question, embedder, collection, request_id=None):
    queries = generate_queries(question)
    seen = set()
    top_chunks = []

    for q in queries:
        embedding = embedder.encode([q]).tolist()
        results = collection.query(query_embeddings=embedding, n_results=3)
        for chunk in results["documents"][0]:
            if chunk not in seen:
                seen.add(chunk)
                top_chunks.append(chunk)
            if len(top_chunks) >= 5:
                break

    if not top_chunks:
        return [], "No relevant context found."

    context = "\n---\n".join(top_chunks)
    prompt = f"Use the following information to answer the question:\n{context}\n\nQuestion: {question}\nAnswer:"
    answer = query_phi(prompt)
    return top_chunks, answer
