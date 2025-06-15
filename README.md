# PhiChat (FastAPI + GGUF + llama.cpp)

This project provides a simple web interface to interact with the **Phi-3 Mini** language model in **GGUF** format using **FastAPI** and `llama-cpp-python`, enhanced with **RAG (Retrieval Augmented Generation)** using **ChromaDB** for document search, and file upload functionality for ingesting PDFs.

## 🚀 Features

* Interactive HTML frontend for asking questions
* Local inference using **Phi-3 Mini model** (GGUF)
* **RAG** integration: retrieve relevant documents from uploaded files to enhance answers
* **File upload**: Upload and ingest PDF or TXT files for context
* Chat history persisted to CSV (`chat_log.csv`)
* Console logging of all interactions

---

## 🧪 Running the App

### 1. Install the required dependencies:

Ensure you have Python 3.8+ installed. Then, install the necessary libraries by running:

```bash
pip install -r requirements.txt
```

### 2. Start the FastAPI server:

Start the server using Uvicorn:

```bash
uvicorn main:app --reload
```

### 3. Open the app in your browser:

Go to:

```
http://127.0.0.1:8000
```

---

## 📁 File Structure

```
PHICHAT/
├── chat_log/
│ ├── chat_log.csv # CSV file containing chat history
│ └── chat_log.py # Script for handling chat logs
├── llm_model/ # LLM backend or library files
│ └── Phi-3-mini-4k-instruct...# LLM model file (Phi-3)
├── rag/
│ ├── strategies/ # Different RAG strategies implemented
│ │ ├── init.py
│ │ ├── basic.py
│ │ ├── llm_only.py
│ │ ├── multiquery.py
│ │ ├── query_rewrite.py
│ │ └── rerank.py
│ ├── llm.py # LLM-related utility functions
│ └── utils.py # General utility functions
├── ui/
│ └── html_template.py # HTML rendering template
├── app.py # UI entry point or main server logic
└── requirements.txt # Python dependencies
```
---

## 🧠 How It Works

* The FastAPI app allows you to ask questions via a web form.
* **File Upload**: You can upload PDF file, which are parsed and stored in a ChromaDB collection. This enables the system to retrieve relevant documents to improve answers.
* **RAG (Retrieval Augmented Generation)**: When a question is asked, it checks the uploaded documents for related content and appends it to the prompt sent to the Phi-3 model.
* The **Phi-3 Mini** model (in GGUF format) generates answers to the questions based on the context and question.
* The **chat history** (including questions, answers, and request IDs) is saved to a CSV file for later reference.

### Steps for asking questions:

1. The user enters a question in the input box.
2. The system retrieves relevant documents from the uploaded files.
3. The question and retrieved context are sent to the Phi-3 Mini model.
4. The generated answer is displayed.
5. The question, answer, and request ID are logged to chat_log.csv.

### Steps for uploading files:

1. You can upload a PDF file via the upload form.
2. The system extracts and chunks the text content of the file into smaller pieces.
3. The system generates embeddings for each chunk and stores them in a **ChromaDB** collection.
4. These chunks are then available for retrieval when asking questions.

### Steps for selecting RAG technique:

1. You can upload a PDF file via the upload form.
2. Select the drop-down menu and choose the RAG technique.

---

## 🔧 Requirements

* **FastAPI**: For building the web application
* **Uvicorn**: For running the FastAPI server
* **llama-cpp-python**: For loading and interacting with the Phi-3 Mini GGUF model
* **Sentence-Transformers**: For generating embeddings from text
* **ChromaDB**: For storing and querying document chunks
* **PyMuPDF (fitz)**: For PDF text extraction
* **pandas**: For managing chat history in CSV format

---

## 📝 Notes

* Ensure you have the **Phi-3 Mini model (GGUF format)** downloaded and placed in the project directory.
* The uploaded files are stored temporarily in memory and are chunked for efficient retrieval.
* **Chat history** is saved to a CSV file (`chat_log.csv`) and can be reviewed on the main page.
