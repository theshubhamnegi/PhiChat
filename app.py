from fastapi import FastAPI, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from llama_cpp import Llama
import uuid
import logging
import pandas as pd
import os
from sentence_transformers import SentenceTransformer
import chromadb
import fitz # for pdf reading

app = FastAPI()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

# for the history of chats
csv_path = "chat_log.csv"
if os.path.exists(csv_path):
    chat_history = pd.read_csv(csv_path)
else:
    chat_history = pd.DataFrame(columns=["id", "question", "answer"])

# web app format
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>PhiChat with RAG</title></head>
<body>
    <h2>Ask PhiChat</h2>
    <form action="/ask" method="post">
        <input type="text" name="question" placeholder="Your question" style="width: 300px;" required>
        <button type="submit">Ask</button>
    </form>

    <hr>
    <h3>Upload a File (PDF or TXT)</h3>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="file" accept="application/pdf" required>
        <button type="submit">Upload & Ingest</button>
        {status}
    </form>

    <hr>
    <h3>Answer</h3>
    {result}

    <hr>
    <h3>History</h3>
    {chat_history}
</body>
</html>
"""

# phi3 model and chromaDB
llm = Llama(model_path="Phi-3-mini-4k-instruct-q4.gguf", n_ctx=4096, n_threads=4)
embedder = SentenceTransformer("all-MiniLM-L6-v2")
chroma_client = chromadb.Client()
rag_collection = chroma_client.get_or_create_collection("rag-data")

# phi3 input and output
def query_phi(prompt: str) -> str:
    full_prompt = f"<|user|>\n{prompt}\n<|assistant|>\n"
    output = llm(full_prompt, max_tokens=1024, stop=["<|user|>"], echo=False)
    return output["choices"][0]["text"].strip()

# retreive chat history
def render_chat_history():
    if chat_history.empty:
        return "<p>No previous questions yet.</p>"
    rows = [
        f"<p><strong>ID:</strong> {row['id']}<br><strong>Q:</strong> {row['question']}<br><strong>A:</strong> {row['answer']}</p>"
        for _, row in chat_history.iterrows()
    ]
    return "".join(rows)

# extract text from pdf
def extract_text(file: UploadFile) -> str:
    file.file.seek(0) # this reset the file reading if already read
    doc = fitz.open(stream=file.file.read(), filetype="pdf")
    return "\n".join(page.get_text() for page in doc)

# text chuncking
def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

# routes
@app.get("/", response_class=HTMLResponse)
async def index():
    return HTML_TEMPLATE.format(status="", result="", chat_history=render_chat_history())

@app.post("/ask", response_class=HTMLResponse)
async def ask(question: str = Form(...)):
    global chat_history

    request_id = str(uuid.uuid4())
    query_embedding = embedder.encode(question).tolist()

    # top 3 results : change n-result to the number of number of head results
    results = rag_collection.query(query_embeddings=[query_embedding], n_results=3)
    context = "\n".join(results["documents"][0]) if results["documents"] else ""
    
    prompt = f"{context}\nUser: {question}\nAssistant:"
    response = query_phi(prompt)

    logging.info(f"[{request_id}] User Query: {question}")
    logging.info(f"[{request_id}] LLM Response: {response}")

    # savingg history
    chat_history.loc[len(chat_history)] = [request_id, question, response]
    chat_history.to_csv(csv_path, index=False)

    result_html = f"""
    <p><strong>ID:</strong> {request_id}</p>
    <p><strong>Question:</strong> {question}</p>
    <p><strong>Answer:</strong> {response}</p>
    """
    
    return HTML_TEMPLATE.format(status="", result=result_html, chat_history=render_chat_history())

@app.post("/upload", response_class=HTMLResponse)
async def upload(file: UploadFile = File(...)):
    status = ""
    
    text = extract_text(file)
    chunks = chunk_text(text)

    embeddings = embedder.encode(chunks).tolist()
    ids = [str(uuid.uuid4()) for _ in chunks]

    rag_collection.add(documents=chunks, ids=ids, embeddings=embeddings)

    status = f"<p>File <strong>{file.filename}</strong> ingested successfully with {len(chunks)} chunks.</p>"

    return HTML_TEMPLATE.format(status=status, result="", chat_history=render_chat_history())