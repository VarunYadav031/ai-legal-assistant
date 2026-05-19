import os
from google import genai

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None


def offline_summary():
    return "⚠️ AI temporarily unavailable (quota / API issue)."


def call_gemini(prompt):

    if not client:
        print("❌ No API key found")
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

            # SAFE HANDLING
            if response and hasattr(response, "text") and response.text:
                return response.text.strip()

        except Exception as e:
            print(f"❌ Model failed ({model}):", str(e))

    return None


def summarize_legal_document(text: str, style="simple", language="english"):

    if not text or len(text.strip()) < 50:
        return "❌ No sufficient document text found"

    if not client:
        return "❌ GEMINI_API_KEY missing"

    text = text[:8000]  # safer limit

    prompt = f"""
You are a legal document summarizer.

STYLE: {style}
LANGUAGE: {language}

RULES:
- Only use document
- Do not hallucinate
- Be structured

DOCUMENT:
{text}
"""

    result = call_gemini(prompt)

    if not result:
        print("⚠️ Gemini returned empty response")
        return offline_summary()

    return result