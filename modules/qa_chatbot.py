import os
from google import genai
from modules.vector_store import vs

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not set")

client = genai.Client(api_key=api_key)


def ask_question(question: str):

    context_chunks = vs.search(question, n_results=4)
    context_text = "\n".join(context_chunks)

    prompt = f"""
You are a legal assistant AI.

Use context to answer.

Context:
{context_text}

Question:
{question}

Answer in simple language.
"""

    response = client.models.generate_content(
        model="gemini-2.0-flash",   # ✅ FIXED MODEL
        contents=prompt
    )

    return response.text