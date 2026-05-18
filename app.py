import streamlit as st

from modules.extractor import extract_text_from_pdf
from modules.summarizer import summarize_legal_document
from modules.qa_chatbot import ask_question
from modules.vector_store import vs

# ✅ KEYPOINTS IMPORT (ADDED AS YOU ASKED)
from modules.key_points import keypoint_extractor


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
    st.info("RAG + ChromaDB + Gemini + Keypoints Engine")


# ===================== SUMMARIZER (UPDATED) =====================
elif page == "📄 Summarizer":

    st.title("📄 Document Analyzer (RAG + Keypoints)")

    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

    if uploaded_file:

        # ---------------- EXTRACT TEXT ----------------
        text = extract_text_from_pdf(uploaded_file)

        st.success("File loaded successfully!")

        # ---------------- RAW PREVIEW ----------------
        with st.expander("📄 Raw Text Preview"):
            st.write(text[:2000])

        # ---------------- KEYPOINTS (NEW FEATURE) ----------------
        st.subheader("🔥 Key Legal Points")

        try:
            keypoints = keypoint_extractor.extract_keypoints(text)

            if keypoints:
                for i, point in enumerate(keypoints):
                    st.markdown(f"**{i+1}.** {point}")
            else:
                st.warning("No key points found.")

        except Exception as e:
            st.error(f"Keypoints error: {e}")

        # ---------------- VECTOR STORE (FAST + ONCE ONLY) ----------------
        if "doc_id" not in st.session_state:
            st.session_state.doc_id = None

        current_id = hash(text)

        if st.session_state.doc_id != current_id:
            vs.add_documents([text])
            st.session_state.doc_id = current_id

        # ---------------- SUMMARY ----------------
        if st.button("Generate Summary"):

            with st.spinner("Generating summary..."):

                summary = summarize_legal_document(text[:3500])

            st.subheader("📌 Summary")
            st.write(summary)

            st.download_button(
                "Download Summary",
                summary,
                file_name="summary.txt"
            )


# ===================== CHAT =====================
elif page == "💬 Legal Chat":

    st.title("💬 Legal AI Chatbot (RAG System)")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_question = st.text_input("Ask your legal question:")

    if st.button("Ask") and user_question:

        with st.spinner("Thinking..."):

            answer = ask_question(user_question)

        st.session_state.chat_history.append(("🧑 You", user_question))
        st.session_state.chat_history.append(("⚖️ AI", answer))

    for role, msg in st.session_state.chat_history:
        st.markdown(f"**{role}:** {msg}")