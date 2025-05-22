from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from llama_cpp import Llama
import uuid
import logging
import pandas as pd
import os

app = FastAPI()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

csv_path = "chat_log.csv"
if os.path.exists(csv_path):
    chat_history = pd.read_csv(csv_path)
else:
    chat_history = pd.DataFrame(columns=["id", "question", "answer"])

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>PhiChat</title></head>
<body>
    <h2>Ask to PhiChat</h2>
    <form action="/ask" method="post">
        <input type="text" name="question" placeholder="Your question" style="width: 300px;" required>
        <button type="submit">Ask</button>
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

llm = Llama(model_path="Phi-3-mini-4k-instruct-q4.gguf", n_ctx=4096, n_threads=4)

def query_phi(prompt: str) -> str:
    full_prompt = f"<|user|>\n{prompt}\n<|assistant|>\n"
    output = llm(full_prompt, max_tokens=1024, stop=["<|user|>"], echo=False)
    return output["choices"][0]["text"].strip()


def render_chat_history():
    if chat_history.empty:
        return "<p>No previous questions yet.</p>"
    rows = [
        f"<p><strong>ID:</strong> {row['id']}<br><strong>Q:</strong> {row['question']}<br><strong>A:</strong> {row['answer']}</p>"
        for _, row in chat_history.iterrows()
    ]
    return "".join(rows)

@app.get("/", response_class=HTMLResponse)
async def index():
    return HTML_TEMPLATE.format(result="", chat_history=render_chat_history())

@app.post("/ask", response_class=HTMLResponse)
async def ask(question: str = Form(...)):
    global chat_history

    request_id = str(uuid.uuid4())
    response = query_phi(question)

    logging.info(f"[{request_id}] User Query: {question}")
    logging.info(f"[{request_id}] LLM Response: {response}")

    chat_history.loc[len(chat_history)] = [request_id, question, response]
    chat_history.to_csv(csv_path, index=False)

    result_html = f"""
    <p><strong>ID:</strong> {request_id}</p>
    <p><strong>Question:</strong> {question}</p>
    <p><strong>Answer:</strong> {response}</p>
    """
    
    return HTML_TEMPLATE.format(result=result_html, chat_history=render_chat_history())