from rag.llm import query_phi
import numpy as np

def reciprocal_rank_fusion(results, k=60):
    """
    Combine multiple ranked lists using Reciprocal Rank Fusion.
    results: list of lists of (doc, score) or just list of docs (if ranked)
    """
    fused_scores = {}
    
    for rank_list in results:
        for rank, doc in enumerate(rank_list):
            if doc not in fused_scores:
                fused_scores[doc] = 0
            fused_scores[doc] += 1 / (rank + k)
            
    reranked = sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)
    return [doc for doc, score in reranked]

def run(question, embedder, collection, request_id=None, **kwargs):
    bm25 = kwargs.get("bm25")
    chunks = kwargs.get("chunks") # raw documents list corresponding to bm25
    
    if not bm25 or not chunks:
        # Fallback to basic if bm25 not available
        return basic_search(question, embedder, collection)
    
    # 1. Semantic Search
    embedding = embedder.encode([question]).tolist()
    sem_results = collection.query(query_embeddings=embedding, n_results=5)
    sem_docs = sem_results["documents"][0]
    
    # 2. Keyword Search (BM25)
    tokenized_query = question.split() # Simple splitting, better to use same tokenizer as index
    # bm25.get_top_n returns the actual documents
    kw_docs = bm25.get_top_n(tokenized_query, chunks, n=5)
    
    # 3. Hybrid Fusion (RRF)
    # RRF expects lists of items. items must be hashable (strings are fine).
    fused_docs = reciprocal_rank_fusion([sem_docs, kw_docs])
    top_chunks = fused_docs[:3]
    
    if not top_chunks:
        return [], "No relevant context found."

    context = "\n---\n".join(top_chunks)
    prompt = f"Use the following information to answer the question:\n{context}\n\nQuestion: {question}\nAnswer:"
    answer = query_phi(prompt)
    return top_chunks, answer

def basic_search(question, embedder, collection):
    embedding = embedder.encode([question]).tolist()
    results = collection.query(query_embeddings=embedding, n_results=3)
    top_chunks = results["documents"][0]
    
    if not top_chunks:
        return [], "No relevant context found."

    context = "\n---\n".join(top_chunks)
    prompt = f"Use the following information to answer the question:\n{context}\n\nQuestion: {question}\nAnswer:"
    answer = query_phi(prompt)
    return top_chunks, answer
