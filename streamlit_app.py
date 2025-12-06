import streamlit as st
import uuid
import pandas as pd
import os
from sentence_transformers import SentenceTransformer
import chromadb
from chat_log.chat_log import load_chat_history, log_interaction
from rag.utils import extract_text, chunk_text
from rag.strategies import run_rag_strategy
from rank_bm25 import BM25Okapi

# Page Config
st.set_page_config(page_title="PhiChat", page_icon="🤖", layout="wide")

# Initialize Resources (Cached)
@st.cache_resource
def load_resources():
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    chroma_client = chromadb.Client()
    rag_collection = chroma_client.get_or_create_collection("rag_data")
    return embedder, rag_collection

embedder, rag_collection = load_resources()

# Sidebar - Configuration & Upload
with st.sidebar:
    st.title("⚙️ Configuration")
    
    # RAG Strategy Selection
    # RAG Strategy Selection
    strategy_display_map = {
        "LLM Only": "llm_only",
        "Semantic (Basic)": "basic",
        "Hybrid (Semantic + Keyword)": "hybrid",
        "Multi-Query": "multiquery",
        "Query Rewrite": "query_rewrite",
        "Rerank": "rerank"
    }
    selected_strategy_name = st.selectbox(
        "RAG Strategy",
        list(strategy_display_map.keys()),
        index=0
    )
    strategy = strategy_display_map[selected_strategy_name]
    
    st.divider()
    
    # File Upload
    st.subheader("📄 Document Ingestion")
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
    
    if uploaded_file is not None:
        # Check if file is already processed in session state to avoid re-processing on every rerun
        if "processed_file" not in st.session_state or st.session_state.processed_file != uploaded_file.name:
            with st.spinner("Processing document..."):
                try:
                    text = extract_text(uploaded_file)
                    chunks = chunk_text(text)
                    embeddings = embedder.encode(chunks).tolist()
                    ids = [str(uuid.uuid4()) for _ in chunks]
                    
                    rag_collection.add(documents=chunks, ids=ids, embeddings=embeddings)
                    
                    # Compute BM25 Index
                    tokenized_corpus = [chunk.split() for chunk in chunks]
                    bm25 = BM25Okapi(tokenized_corpus)
                    st.session_state.bm25 = bm25
                    st.session_state.chunks = chunks
                    
                    st.session_state.processed_file = uploaded_file.name
                    st.success(f"Ingested {len(chunks)} chunks from {uploaded_file.name}")
                except Exception as e:
                    st.error(f"Error processing file: {str(e)}")

# Main Chat Interface
st.title("🤖 PhiChat")
st.caption("Chat with your documents using Phi-3 and RAG")

# Load Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Load existing history from JSONL
    history = load_chat_history()
    for entry in history:
        st.session_state.messages.append({"role": "user", "content": entry['question']})
        st.session_state.messages.append({"role": "assistant", "content": entry['answer']})

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Ask a question..."):
    # Add user message to state and display
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            request_id = str(uuid.uuid4())
            try:
                # Run RAG Strategy
                bm25 = st.session_state.get("bm25")
                chunks = st.session_state.get("chunks")
                top_chunks, answer = run_rag_strategy(prompt, strategy, embedder, rag_collection, request_id, bm25=bm25, chunks=chunks)
                
                # Update JSONL Log
                log_interaction(request_id, strategy, prompt, answer, source_chunks=top_chunks)
                
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
                
                # Optional: Show source chunks in expander
                with st.expander("View Retrieved Context"):
                    for i, chunk in enumerate(top_chunks):
                        st.markdown(f"**Chunk {i+1}:** {chunk}")
                        
            except Exception as e:
                st.error(f"Error: {str(e)}")
