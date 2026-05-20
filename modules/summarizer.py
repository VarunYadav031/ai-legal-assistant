# modules/summarizer.py

import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

# Load local .env file (works on your local machine)
load_dotenv()


def get_api_key():
    """
    Priority:
    1. Streamlit Cloud secrets
    2. Local .env file
    3. System environment variables
    """
    return (
        st.secrets.get("GEMINI_API_KEY")
        or os.getenv("GEMINI_API_KEY")
    )


# Initialize Gemini client
api_key = get_api_key()
client = genai.Client(api_key=api_key) if api_key else None


def offline_summary():
    return "⚠️ AI temporarily unavailable (quota exceeded or API issue)."


def call_gemini(prompt: str):
    """Call Gemini with fallback models."""

    if not client:
        print("❌ GEMINI_API_KEY not found")
        return None

    models = [
        "gemini-2.0-flash",
        "gemini-1.5-flash"
    ]

    for model in models:
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt
            )

            if response and hasattr(response, "text") and response.text:
                return response.text.strip()

        except Exception as e:
            print(f"❌ Model failed ({model}): {str(e)}")

    return None


def summarize_legal_document(
    text: str,
    style: str = "simple",
    language: str = "english"
):
    """Generate a legal document summary."""

    if not text or len(text.strip()) < 50:
        return "❌ No sufficient document text found."

    if not client:
        return "❌ GEMINI_API_KEY missing."

    # Limit text size for safety
    text = text[:8000]

    prompt = f"""
You are a professional legal document summarizer.

STYLE: {style}
LANGUAGE: {language}

RULES:
- Only use the provided document.
- Do not hallucinate or invent information.
- Keep the summary well-structured.
- Highlight important clauses and obligations.

DOCUMENT:
{text}
"""

    result = call_gemini(prompt)

    if not result:
        print("⚠️ Gemini returned empty response")
        return offline_summary()

    return result