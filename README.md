# PhiChat
````markdown
# PhiChat (FastAPI + GGUF + llama.cpp)

This project provides a simple web interface to interact with the **Phi-3 Mini** language model in **GGUF** format using **FastAPI** and `llama-cpp-python`.

## 🚀 Features

- Interactive HTML frontend for asking questions
- Local inference using Phi-3 Mini model (GGUF)
- Chat history persisted to CSV (`chat_log.csv`)
- Console logging of all interactions
````

## 🧪 Running the App

Start the server using Uvicorn:

```bash
uvicorn main:app --reload
```

Then open your browser and go to:

```
http://127.0.0.1:8000
```

---

## 📁 File Structure

```
.
├── main.py                        # FastAPI app
├── chat_log.csv                  # Chat history (auto-generated)
├── Phi-3-mini-4k-instruct-q4.gguf # GGUF model file (download manually)
└── README.md                     # This file
```

---

## 🧠 How It Works

* Loads the Phi-3 Mini model using `llama-cpp-python`
* Takes user input from a web form
* Sends the question to the model using a formatted prompt
* Displays the answer on the same page
* Saves the question, answer, and request ID to `chat_log.csv`
