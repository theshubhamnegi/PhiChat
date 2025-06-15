from fastapi import FastAPI, Form, UploadFile, File
from fastapi.responses import HTMLResponse
import uuid
import logging
from sentence_transformers import SentenceTransformer
import chromadb
from ui.html_template import HTML_TEMPLATE
from chat_log.chat_log import chat_history, csv_path
from rag.utils import extract_text, chunk_text, render_chat_history
from rag.strategies import run_rag_strategy

# Init App
app = FastAPI()
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

# Init Embedder and DB
embedder = SentenceTransformer("all-MiniLM-L6-v2")
chroma_client = chromadb.Client()
rag_collection = chroma_client.get_or_create_collection("rag_data")

# Routes
@app.get("/", response_class=HTMLResponse)
async def index():
    return HTML_TEMPLATE.format(status="", result="", chat_history=render_chat_history(chat_history))

@app.post("/ask", response_class=HTMLResponse)
async def ask(question: str = Form(...), strategy: str = Form("basic")):
    global chat_history
    request_id = str(uuid.uuid4())

    try:
        top_chunks, answer = run_rag_strategy(question, strategy, embedder, rag_collection, request_id)
        
        chat_history.loc[len(chat_history)] = [request_id, strategy, question, answer]
        chat_history.to_csv(csv_path, index=False)

        result_html = f"""
        <p><strong>ID:</strong> {request_id}</p>
        <p><strong>Strategy:</strong> {strategy}</p>
        <p><strong>Question:</strong> {question}</p>
        <p><strong>Answer:</strong> {answer}</p>
        """

    except Exception as e:
        logging.error(f"[{request_id}] Error: {str(e)}")
        result_html = f"<p style='color:red;'>Error: {str(e)}</p>"

    return HTML_TEMPLATE.format(status="", result=result_html, chat_history=render_chat_history(chat_history))

@app.post("/upload", response_class=HTMLResponse)
async def upload(file: UploadFile = File(...)):
    status = ""
    result = ""
    try:
        text = extract_text(file)
        chunks = chunk_text(text)
        embeddings = embedder.encode(chunks).tolist()
        ids = [str(uuid.uuid4()) for _ in chunks]

        rag_collection.add(documents=chunks, ids=ids, embeddings=embeddings)
        status = f"<p>File <strong>{file.filename}</strong> ingested successfully with {len(chunks)} chunks.</p>"

    except Exception as e:
        status = f"<p style='color:red;'>Error: {str(e)}</p>"

    return HTML_TEMPLATE.format(status=status, result=result, chat_history=render_chat_history(chat_history))
