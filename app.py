import streamlit as st

from modules.extractor import extract_text_from_pdf
from modules.summarizer import summarize_legal_document
from modules.qa_chatbot import ask_question
from modules.vector_store import vs

from modules.key_points import keypoint_extractor
from modules.clause_explainer import clause_explainer


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Legal Assistant",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- SIDEBAR ----------------
page = st.sidebar.radio(
    "Navigate",
    ["🏠 Home", "📄 Summarizer", "💬 Legal Chat"]
)


# ===================== HOME =====================
if page == "🏠 Home":
    st.title("⚖️ AI Legal Assistant")
    st.info("RAG + Smart Memory AI + Multilingual Support")


# ===================== SUMMARIZER =====================
elif page == "📄 Summarizer":

    st.title("📄 Document Analyzer")

    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

    if uploaded_file:

        text = extract_text_from_pdf(uploaded_file)
        st.success("File loaded successfully!")

        with st.expander("Preview"):
            st.write(text[:2000])

        # Keypoints
        st.subheader("🔥 Key Points")
        keypoints = keypoint_extractor.extract_keypoints(text)

        for i, point in enumerate(keypoints):
            st.markdown(f"**{i+1}.** {point}")

        # Clause Explainer
        if keypoints:
            st.subheader("🧠 Clause Explainer")

            for i, clause in enumerate(keypoints[:5]):
                result = clause_explainer.explain_clause(clause)

                st.markdown(f"### Clause {i+1}")
                st.write(f"📌 Original: {result['original']}")
                st.success(f"🧠 Simple: {result['simple']}")
                st.info(f"Category: {result['category']}")

        # Vector DB
        if "doc_id" not in st.session_state:
            st.session_state.doc_id = None

        if st.session_state.doc_id != hash(text):
            vs.add_documents([text])
            st.session_state.doc_id = hash(text)

        # Summary
        if st.button("Generate Summary"):
            summary = summarize_legal_document(text[:3500])
            st.write(summary)
            st.download_button("Download", summary, file_name="summary.txt")


# ===================== CHAT (FULL MULTILINGUAL + MEMORY) =====================
elif page == "💬 Legal Chat":

    st.title("💬 Legal AI Chatbot")

    # ---------------- SESSION INIT ----------------
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "language" not in st.session_state:
        st.session_state.language = "hinglish"

    # ---------------- LANGUAGE SELECTOR ----------------
    st.session_state.language = st.selectbox(
        "Choose Language / भाषा चुनें",
        ["hinglish", "hindi", "english"]
    )

    # ---------------- LANGUAGE SWITCH DETECTOR ----------------
    def detect_language_switch(text):
        text = text.lower()

        if "switch to hindi" in text or "hindi" == text.strip():
            return "hindi"
        if "switch to english" in text or "english" == text.strip():
            return "english"
        if "hinglish" in text:
            return "hinglish"

        return None

    # ---------------- SHOW CHAT HISTORY ----------------
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # ---------------- INPUT ----------------
    user_question = st.chat_input("Ask your legal question...")

    if user_question:

        # detect language switch
        new_lang = detect_language_switch(user_question)
        if new_lang:
            st.session_state.language = new_lang
            st.success(f"Language switched to {new_lang}")

        # save user message
        st.session_state.messages.append({
            "role": "user",
            "content": user_question
        })

        with st.chat_message("user"):
            st.markdown(user_question)

        # AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):

                answer = ask_question(
                    user_question,
                    chat_history=st.session_state.messages,
                    language=st.session_state.language
                )

                st.markdown(answer)

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })