import textwrap
from modules.vector_store import vs


# ---------------- CHUNKING ----------------
def chunk_text(text, chunk_size=800, overlap=150):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap  # overlap for context continuity

    return chunks


# ---------------- INGEST DOCUMENT ----------------
def ingest_document(text):
    chunks = chunk_text(text)

    vs.add_documents(chunks)

    return len(chunks)


# ---------------- RETRIEVE CONTEXT ----------------
def retrieve_context(query, top_k=3):
    return vs.search(query, n_results=top_k)


# ---------------- BUILD PROMPT ----------------
def build_prompt(question, context_chunks):
    context = "\n\n".join(context_chunks)

    prompt = f"""
You are a legal AI assistant.

Use the given context to answer the question.

Context:
{context}

Question:
{question}

Rules:
- Answer clearly
- Use simple legal explanation
- If not found, say "Not available in document"

Answer:
"""
    return prompt