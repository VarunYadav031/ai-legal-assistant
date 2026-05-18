import os
from google import genai
from modules.vector_store import vs

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key) if api_key else None


# ---------------- MAIN AI FUNCTION ----------------
def ask_question(question: str, chat_history=None, language="hinglish"):

    # RAG
    context_chunks = vs.search(question, n_results=4)
    context_text = "\n".join(context_chunks) if context_chunks else ""

    # MEMORY
    memory_text = ""
    if chat_history:
        memory_text = "\n".join(
            [f"{m['role']}: {m['content']}" for m in chat_history[-6:]]
        )

    # LANGUAGE CONTROL
    if language == "hindi":
        lang_rule = "Answer ONLY in Hindi."
    elif language == "english":
        lang_rule = "Answer ONLY in English."
    else:
        lang_rule = "Answer in Hinglish (Hindi + English mix)."

    prompt = f"""
You are a Legal AI Assistant.

{lang_rule}

Rules:
- Do not copy full document
- Be simple and clear

Conversation Memory:
{memory_text}

Document Context:
{context_text}

Question:
{question}

Answer:
"""

    # ---------------- GEMINI ----------------
    if client:
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )
            return response.text
        except:
            pass

    # ---------------- FALLBACK ----------------
    q = question.lower()

    if language == "hindi":
        return "📌 दस्तावेज़ के अनुसार कर्मचारी को कॉन्ट्रैक्ट के नियम मानने होते हैं।"

    if language == "english":
        return "📌 Employee must follow contract terms and maintain confidentiality."

    return "📌 Employee ko contract ke rules follow karne hote hain aur confidential info protect karni hoti hai."