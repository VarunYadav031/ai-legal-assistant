import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def summarize_document(text: str) -> str:
    if not text:
        return "No text found"

    text = text[:10000]

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""
You are a legal assistant.

Summarize this legal document clearly:
- Parties
- Key terms
- Obligations
- Risks

Document:
{text}
"""
    )

    return response.text