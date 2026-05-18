import streamlit as st
from modules.extractor import extract_text_from_pdf
from modules.summarizer import summarize_legal_document
from modules.qa_chatbot import ask_question
from modules.vector_store import vs

st.set_page_config(
    page_title="AI Legal Assistant",
    page_icon="⚖️",
    layout="wide"
)

# ---------------- SIDEBAR ----------------
page = st.sidebar.radio(
    "Navigate",
    ["🏠 Home", "📄 Summarizer", "💬 Legal Chat"]
)

# ---------------- HOME ----------------
if page == "🏠 Home":
    st.title("⚖️ AI Legal Document Assistant")
    st.info("Built with Gemini + RAG + Vector DB + Streamlit")

# ---------------- SUMMARIZER ----------------
elif page == "📄 Summarizer":
    st.title("📄 Legal Document Summarizer")

    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

    if uploaded_file:
        text = extract_text_from_pdf(uploaded_file)

        st.success("File processed successfully!")

        with st.expander("Preview"):
            st.write(text[:3000])

        # ✅ RESET DOC STATE FOR NEW FILE
        st.session_state["doc_added"] = False

        # ✅ ADD TO VECTOR STORE ONLY ONCE
        if not st.session_state.get("doc_added", False):
            vs.add_documents([text])
            st.session_state["doc_added"] = True

        # ---------------- SUMMARY ----------------
        if st.button("Generate Summary"):
            with st.spinner("Generating summary..."):
                summary = summarize_legal_document(text)

            st.success("Summary Ready!")

            st.write(summary)

            st.download_button(
                "Download",
                summary,
                file_name="summary.txt"
            )

# ---------------- CHAT ----------------
elif page == "💬 Legal Chat":
    st.title("💬 Legal AI Chatbot (RAG)")

    if not vs.docs:
        st.warning("⚠️ Please upload a PDF first in Summarizer")

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