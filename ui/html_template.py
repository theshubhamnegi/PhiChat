HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>PhiChat with RAG</title></head>
<body>
    <h2>Ask PhiChat</h2>
    <form action="/ask" method="post">
        <input type="text" name="question" placeholder="Your question" style="width: 300px;" required>
        <select name="strategy">
            <option value="llm_only">LLM Only</option>
            <option value="basic">Basic</option>
            <option value="rerank">Re-rank</option>
            <option value="query_rewrite">Query Rewriting</option>
            <option value="multiquery">Multi-query</option>
        </select>
        <button type="submit">Ask</button>
    </form>
    <hr>
    <h3>Upload a File (PDF)</h3>
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
