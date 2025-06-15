import pandas as pd
import os

os.makedirs("chat_log", exist_ok=True)
csv_path = "chat_log/chat_log.csv"

if os.path.exists(csv_path):
    chat_history = pd.read_csv(csv_path)
else:
    chat_history = pd.DataFrame(columns=["id", "strategy", "question", "answer"])