import fitz

def extract_text(file):
    # Handle FastAPI UploadFile
    if hasattr(file, "file"):
        content = file.file.read()
    # Handle Streamlit UploadedFile or standard file object
    else:
        content = file.read()
        # Reset cursor if possible, though usually read once
        if hasattr(file, "seek"):
            file.seek(0)
            
    doc = fitz.open(stream=content, filetype="pdf")
    return "\n".join(page.get_text() for page in doc)

def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size - overlap)]

def render_chat_history(df):
    if df.empty:
        return "<p>No previous questions yet.</p>"
    return "".join(
        f"<p><strong>ID:</strong> {row['id']}<br><strong>ID:</strong> {row['strategy']}<br><strong>Q:</strong> {row['question']}<br><strong>A:</strong> {row['answer']}</p>"
        for _, row in df.iterrows()
    )
