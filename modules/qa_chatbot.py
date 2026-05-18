import os
from google import genai
from modules.vector_store import vs

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def ask_question(question: str):

    # ⚡ reduced retrieval (FAST)
    context_chunks = vs.search(question, n_results=2)

    context_text = "\n".join(context_chunks[:2])

    prompt = f"""
You are a legal assistant.

Context:
{context_text}

Question:
{question}

Answer in simple language.
"""

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )

    return response.text