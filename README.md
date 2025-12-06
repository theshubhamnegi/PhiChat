# PhiChat (Streamlit + FastAPI + GGUF + llama.cpp)

This project provides a **RAG (Retrieval Augmented Generation)** powered chat interface using **Phi-3 Mini** (GGUF format) and **ChromeDB**.
It features a modern **Streamlit UI** for interaction and a separate **FastAPI** backend for API access.

## 🚀 Features

* **Streamlit UI**: A clean, interactive web interface for chatting and file management.
* **Hybrid Search**: Combines **BM25 Keyword Search** and **Semantic Search** (Embeddings) for better retrieval.
* **Local Inference**: Runs **Phi-3 Mini** locally using `llama-cpp-python`.
* **JSONL Logging**: Chat history is saved in `chat_log.jsonl` with full context retrieval data.
* **FastAPI Backend**: A pure JSON API for programmatic access.
* **RAG Strategies**: Support for various strategies including LLM Only, Basic (Semantic), Hybrid, Multi-Query, etc.

---

## 🧪 Running the App

### 1. Install Dependencies:

Ensure Python 3.8+ is installed.

```bash
pip install -r requirements.txt
```

### 2. Run the Streamlit App (UI):

This is the main interface for users.

```bash
streamlit run streamlit_app.py
```

Open your browser at `http://localhost:8501`.

### 3. Run the FastAPI Backend (Optional):

If you want to use the API endpoints.

```bash
uvicorn fastapi_app:app --reload
```

---

## 📁 File Structure

```
PHICHAT/
├── chat_log/
│   ├── chat_log.jsonl     # Chat history with context logs
│   └── chat_log.py        # Logger utility
├── llm_model/             # Place your GGUF model here
├── rag/
│   ├── strategies/        # RAG implementation strategies
│   │   ├── hybrid.py      # BM25 + Semantic implementation
│   │   └── ...
│   └── utils.py           # Text extraction and chunking
├── streamlit_app.py       # Main Streamlit application
├── fastapi_app.py         # JSON API backend
└── requirements.txt       # Dependencies
```

---

## 🧠 How It Works

1.  **Ingestion**: Upload a PDF via the sidebar. Text is extracted, chunked, embedded (ChromaDB), and indexed (BM25).
2.  **Strategy**: Select a RAG strategy. **LLM Only** is default. **Hybrid** uses Reciprocal Rank Fusion to combine keyword and semantic results.
3.  **Generation**: The context is retrieved and sent to Phi-3 to answer your question.
4.  **Logging**: Interactions are saved to `chat_log.jsonl` for review.

## 🔧 Requirements

*   `streamlit`
*   `fastapi`, `uvicorn`
*   `llama-cpp-python`
*   `sentence-transformers`, `chromadb`
*   `rank_bm25` (for Hybrid search)
*   `PyMuPDF`
