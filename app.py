import pandas as pd
import streamlit as st
from streamlit_mic_recorder import mic_recorder

from modules.extractor import extract_text_from_pdf
from modules.summarizer import summarize_legal_document
from modules.qa_chatbot import ask_question
from modules.table_reader import extract_table_insights
from modules.speech_to_text import transcribe_audio
from modules.ingestion import ingest_document
from modules.vector_store import vs


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Lex AI Legal Intelligence",
    page_icon="⚖️",
    layout="wide"
)

# ---------------- CUSTOM UI STYLE ----------------
st.markdown("""
<style>
.main {
    background-color: #0f172a;
    color: white;
}

.block-container {
    padding-top: 2rem;
}

.stButton>button {
    background-color: #1e293b;
    color: white;
    border-radius: 10px;
    padding: 10px 15px;
}

.stChatMessage {
    border-radius: 12px;
    padding: 10px;
}

h1, h2, h3 {
    color: #38bdf8;
}
</style>
""", unsafe_allow_html=True)


# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "language" not in st.session_state:
    st.session_state.language = "hinglish"

if "last_input" not in st.session_state:
    st.session_state.last_input = ""


# ---------------- CHAT FUNCTION ----------------
def process_question(user_question):

    if user_question == st.session_state.last_input:
        return

    st.session_state.last_input = user_question

    st.session_state.messages.append({"role": "user", "content": user_question})

    with st.chat_message("user"):
        st.markdown(user_question)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing legal document... ⚖️"):

            try:
                answer = ask_question(
                    user_question,
                    chat_history=st.session_state.messages,
                    language=st.session_state.language
                )
            except Exception as e:
                answer = f"⚠️ System Error: {str(e)}"

            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})


# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("⚖️ Lex AI System")

    st.markdown("### Smart Legal AI Platform")

    page = st.radio(
        "Select Module",
        ["🏠 Dashboard", "📄 Document AI", "📊 Data Analyzer", "💬 Legal Chat"]
    )


# ---------------- DASHBOARD ----------------
if page == "🏠 Dashboard":
    st.title("⚖️ Legal AI Intelligence System")

    st.info("Upload legal documents, ask questions, generate summaries, and analyze data.")

    col1, col2, col3 = st.columns(3)

    col1.metric("AI Mode", "Gemini + RAG")
    col2.metric("Vector DB", "FAISS")
    col3.metric("Status", "Active")


# ---------------- DOCUMENT AI ----------------
elif page == "📄 Document AI":

    st.title("📄 Legal Document Engine")

    file = st.file_uploader("Upload Legal PDF", type=["pdf"])

    if file:

        text = extract_text_from_pdf(file)

        if not text:
            st.error("Cannot read PDF properly")
            st.stop()

        st.success("Document loaded")

        with st.expander("Preview"):
            st.write(text[:1500])

        if st.button("📥 Store Document in AI Memory"):
            chunks = ingest_document(text)
            vs.add([text])
            st.success(f"Stored {chunks} chunks into memory")

        style = st.selectbox("Summary Style", ["simple", "detailed", "bullet"])
        language = st.selectbox("Language", ["english", "hindi", "hinglish"])

        if st.button("Generate Summary"):
            with st.spinner("Generating AI Summary..."):
                summary = summarize_legal_document(text, style, language)

            st.success("Summary Ready")
            st.write(summary)

            st.download_button("Download Summary", summary, "summary.txt")


# ---------------- DATA ANALYZER ----------------
elif page == "📊 Data Analyzer":

    st.title("📊 Legal Data Intelligence")

    file = st.file_uploader("Upload CSV/XLSX", type=["csv", "xlsx"])

    if file:

        df = pd.read_csv(file) if file.name.endswith(".csv") else pd.read_excel(file)

        st.dataframe(df)

        insights = extract_table_insights(file)

        query = st.text_input("Ask question about data")

        if query:
            answer = ask_question(query + str(insights), language="hinglish")
            st.success(answer)


# ---------------- CHAT ----------------
elif page == "💬 Legal Chat":

    st.title("💬 AI Legal Assistant Chat")

    st.session_state.language = st.selectbox(
        "Response Language",
        ["hinglish", "hindi", "english"]
    )

    st.markdown("### Quick Actions")
    col1, col2, col3 = st.columns(3)

    if col1.button("Confidentiality Clause"):
        process_question("Explain confidentiality clause")

    if col2.button("Employee Duties"):
        process_question("What are employee duties?")

    if col3.button("Termination Terms"):
        process_question("Explain termination terms")

    st.divider()

    # CHAT HISTORY
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).markdown(msg["content"])

    # VOICE INPUT
    audio = mic_recorder(start_prompt="🎙 Speak", stop_prompt="Stop")

    if audio and "bytes" in audio:
        with open("temp.wav", "wb") as f:
            f.write(audio["bytes"])

        text = transcribe_audio("temp.wav")

        if text:
            st.success(f"You said: {text}")
            process_question(text)

    # TEXT INPUT
    user_input = st.chat_input("Ask legal question...")

    if user_input:
        process_question(user_input)
    
try:
    st.write("API key found:", bool(st.secrets["GEMINI_API_KEY"]))
except Exception:
    st.write("API key found:", False)