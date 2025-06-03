# Error Message
ChromaDB dimension mismatch error

## Root Cause of the Error
The embedding vectors generated during document ingestion used a different model or version than the one used during querying, causing dimension mismatch between stored and query vectors.

## Different Approaches Tried Out
**First Approach**:
- Attempted to query the existing ChromaDB collection without modifying the embedding pipeline.

**Second Approach**:
- Deleted the current ChromaDB collection and re-ingested all documents using embeddings from the current and consistent SentenceTransformer model.

## Selected Approach and Why?
Re-ingested documents into a fresh ChromaDB collection using the same embedding model as used during querying.

**Reason for Selection**:
- Ensures dimensional consistency between query embeddings and stored vectors, eliminating errors at query time.

- Prevents future issues when switching between models or upgrading libraries that affect embedding size.

## Result
After re-ingesting with consistent embedding dimensions, ChromaDB successfully returns relevant documents during queries. RAG pipeline functions reliably.