import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def summarize_legal_document(text: str) -> str:
    """
    Legal document summarizer using Gemini
    """

    if not text:
        return "No text found"

    text = text[:10000]  # safety limit

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""
You are a professional legal AI assistant.

Summarize this legal document in simple terms:

1. Parties involved
2. Key clauses
3. Obligations
4. Risks
5. Simple explanation for non-lawyers

Document:
{text}
"""
    )

    return response.text