from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
import uuid
import logging
from sentence_transformers import SentenceTransformer
import chromadb
from chat_log.chat_log import log_interaction
from rag.utils import extract_text, chunk_text
from rag.strategies import run_rag_strategy

# Init App
app = FastAPI(title="PhiChat API")
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

# Init Embedder and DB
embedder = SentenceTransformer("all-MiniLM-L6-v2")
chroma_client = chromadb.Client()
rag_collection = chroma_client.get_or_create_collection("rag_data")

@app.get("/")
async def health_check():
    return {"status": "ok", "message": "PhiChat API is running"}

@app.post("/ask")
async def ask(question: str = Form(...), strategy: str = Form("llm_only")):
    request_id = str(uuid.uuid4())
    try:
        top_chunks, answer = run_rag_strategy(question, strategy, embedder, rag_collection, request_id)
        
        # Log to JSONL
        log_interaction(request_id, strategy, question, answer, source_chunks=top_chunks)
        
        return {
            "request_id": request_id,
            "strategy": strategy,
            "question": question,
            "answer": answer,
            "context": top_chunks
        }
    except Exception as e:
        logging.error(f"[{request_id}] Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        text = extract_text(file)
        chunks = chunk_text(text)
        embeddings = embedder.encode(chunks).tolist()
        ids = [str(uuid.uuid4()) for _ in chunks]

        rag_collection.add(documents=chunks, ids=ids, embeddings=embeddings)
        return {
            "status": "success",
            "filename": file.filename,
            "chunks_ingested": len(chunks)
        }
    except Exception as e:
        logging.error(f"Error uploading file: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
