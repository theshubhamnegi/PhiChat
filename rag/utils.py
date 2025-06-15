import fitz

def extract_text(file):
    doc = fitz.open(stream=file.file.read(), filetype="pdf")
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
