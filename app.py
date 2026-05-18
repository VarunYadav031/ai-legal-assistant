import streamlit as st
from modules.extractor import extract_text_from_pdf
from modules.summarizer import summarize_legal_document

st.set_page_config(
    page_title="AI Legal Assistant",
    page_icon="⚖️",
    layout="wide"
)

# ---------------- SIDEBAR ----------------
st.sidebar.title("⚖️ Legal AI Assistant")
page = st.sidebar.radio(
    "Navigate",
    ["🏠 Home", "📄 Summarizer", "💬 Chat (Coming Soon)"]
)

# ---------------- HOME ----------------
if page == "🏠 Home":
    st.title("⚖️ AI Legal Document Assistant")
    st.markdown("Upload legal documents and analyze them using AI.")

    st.info("Built with Gemini + RAG + ChromaDB (Upgrading...)")

# ---------------- SUMMARIZER ----------------
elif page == "📄 Summarizer":
    st.title("📄 Legal Document Summarizer")

    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

    if uploaded_file:
        text = extract_text_from_pdf(uploaded_file)

        st.success("File processed successfully!")

        with st.expander("📑 Preview Text"):
            st.write(text[:3000])

        if st.button("🚀 Generate Summary"):
            with st.spinner("AI analyzing document..."):
                summary = summarize_legal_document(text)

            st.success("Summary Ready!")

            st.markdown("### 🧠 AI Summary")
            st.write(summary)

            st.download_button(
                "⬇️ Download Summary",
                summary,
                file_name="legal_summary.txt"
            )