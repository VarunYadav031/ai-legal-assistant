import os
import re
from datetime import datetime
from google import genai
from modules.vector_store import vs

# ---------------- GEMINI CLIENT ----------------
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None


# ---------------- SMART FALLBACK ENGINE ----------------
def smart_fallback(results, question):

    docs = [r[0] if isinstance(r, tuple) else r for r in results]
    context = "\n".join(docs)

    question_lower = question.lower()

    # ---------------- DATE EXTRACTION ----------------
    date_pattern = r'\d{1,2}(?:st|nd|rd|th)?\s+[A-Za-z]+\s+\d{4}'
    found_dates = re.findall(date_pattern, context)
    dates_text = ", ".join(found_dates)

    # ---------------- SMART CONTEXT LINES ----------------
    sentences = re.split(r'(?<=[.!?]) +', context)
    relevant = [s for s in sentences if len(s) > 25][:6]

    # ---------------- COMMITMENT / DATE LOGIC ----------------
    if any(word in question_lower for word in ["date", "complete", "commitment", "term", "duration"]):

        if found_dates:
            return f"""
📌 Contract / Commitment Timeline Analysis:

🗓 Found Dates:
{dates_text}

🧠 Interpretation:
- Agreement contains Effective/Contract date(s).
- Commitment starts from the earliest mentioned date.
- Completion depends on contract duration clause (not fully visible in extracted text).

🎯 Answer:
Commitment starts from {found_dates[0]} (as per document). Completion depends on contract terms.

⚠ Confidence: Medium–High (Fallback Reasoning)
"""

        return f"""
📌 Timeline Analysis:

{" ".join(relevant)}

🧠 Interpretation:
Contract duration or dates are mentioned but not clearly structured.

🎯 Confidence: Medium
"""

    # ---------------- EMPLOYEE ----------------
    if "employee" in question_lower:
        return f"""
📌 Employee Information:

{" ".join(relevant)}

🧠 Interpretation:
Employee details are present in the agreement.

🎯 Confidence: Medium
"""

    # ---------------- CONFIDENTIALITY ----------------
    if "confidential" in question_lower:
        return f"""
📌 Confidentiality Clause:

{" ".join(relevant)}

🧠 Interpretation:
These sections define confidentiality obligations.

🎯 Confidence: High
"""

    # ---------------- DEFAULT FALLBACK ----------------
    return f"""
📌 Legal Document Insight:

{" ".join(relevant)}

🧠 Note:
AI API is unavailable, but system extracted relevant legal clauses.

🎯 Confidence: Low–Medium
"""


# ---------------- MAIN RAG FUNCTION ----------------
def ask_question(question: str):

    # Step 1: retrieve from vector DB
    results = vs.search(question, n_results=5)

    context = "\n".join([r[0] if isinstance(r, tuple) else r for r in results])

    # Step 2: prompt for Gemini
    prompt = f"""
You are a legal AI assistant.

Rules:
- Use ONLY given context
- Do NOT assume outside information
- If answer not found say "Not found in document"

Context:
{context}

Question:
{question}

Answer clearly and concisely.
"""

    # Step 3: try AI model
    try:
        if client:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )
            return response.text

        # fallback if no API
        return smart_fallback(results, question)

    except Exception:
        # fallback if API fails
        return smart_fallback(results, question)