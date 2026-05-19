import os
from google import genai
from modules.vector_store import vs

# ✅ CACHE SYSTEM
from modules.cache import make_key, get_cache, set_cache


api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None


# ---------------- OFFLINE FALLBACK ----------------
def offline_fallback(question):
    return (
        "⚠️ AI temporarily unavailable.\n\n"
        "Please try again later or rephrase your question."
    )


# ---------------- GEMINI CALL (FIXED + DEBUG) ----------------
def call_gemini(prompt):

    if not client:
        print("❌ Client not initialized (API key missing)")
        return None

    # 🔥 ONLY STABLE MODEL (FIX FOR YOUR ISSUE)
    models = [
        "gemini-2.0-flash"
    ]

    for model in models:
        try:
            res = client.models.generate_content(
                model=model,
                contents=prompt
            )

            # 🔍 DEBUG LOG (IMPORTANT)
            print(f"Model used: {model}")
            print("Response received:", bool(res and res.text))

            if res and res.text and res.text.strip():
                return res.text.strip()

        except Exception as e:
            print(f"❌ Gemini error ({model}):", str(e))
            continue

    return None


# ---------------- MAIN FUNCTION ----------------
def ask_question(question, chat_history=None, language="hinglish"):

    # ================= CACHE CHECK =================
    cache_key = make_key(question)
    cached = get_cache(cache_key)

    if cached:
        return cached + "\n\n⚡ (cached response)"

    # ================= VECTOR SEARCH =================
    context = vs.search(question, n_results=5)

    context_text = "\n\n".join(context) if context else "No relevant context found in document."

    # ================= CHAT MEMORY =================
    memory_text = ""
    if chat_history:
        memory_text = "\n".join(
            [f"{m['role']}: {m['content']}" for m in chat_history[-4:]]
        )

    # ================= LANGUAGE RULE =================
    lang_rule = {
        "hindi": "Answer ONLY in Hindi.",
        "english": "Answer ONLY in English.",
        "hinglish": "Answer in simple Hinglish."
    }.get(language, "Answer in Hinglish.")

    # ================= PROMPT =================
    prompt = f"""
You are a strict legal document AI assistant.

RULES:
- Use ONLY provided context
- If answer not found → say "Not mentioned in document"
- Do NOT use outside knowledge
- Be short and precise

{lang_rule}

CHAT HISTORY:
{memory_text}

CONTEXT:
{context_text}

QUESTION:
{question}

ANSWER:
"""

    # ================= AI RESPONSE =================
    answer = call_gemini(prompt)

    # ================= IMPORTANT FIX (EMPTY RESPONSE SAFETY) =================
    if not answer or answer.strip() == "":
        print("⚠️ Empty response from Gemini")
        answer = offline_fallback(question)

    # ================= SAVE CACHE =================
    set_cache(cache_key, answer)

    return answer