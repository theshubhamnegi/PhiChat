import json
import os
import pandas as pd # Optional, but useful if we ever want to convert to DF

# Ensure directory exists
os.makedirs("chat_log", exist_ok=True)
jsonl_path = "chat_log/chat_log.jsonl"

def log_interaction(request_id, strategy, question, answer, source_chunks=None):
    """
    Appends a new interaction to the JSONL log file.
    """
    entry = {
        "id": request_id,
        "strategy": strategy,
        "question": question,
        "answer": answer,
        "source_chunks": source_chunks if source_chunks else []
    }
    
    with open(jsonl_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

def load_chat_history():
    """
    Loads chat history from the JSONL file.
    Returns a list of dicts.
    """
    if not os.path.exists(jsonl_path):
        return []
    
    history = []
    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                history.append(json.loads(line.strip()))
            except json.JSONDecodeError:
                continue
    return history