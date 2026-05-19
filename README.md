# ⚖️ AI Legal Assistant (RAG + Gemini + FAISS + Streamlit)

An advanced AI-powered Legal Document Intelligence System that allows users to **upload, analyze, summarize, and chat with legal documents** using **Retrieval-Augmented Generation (RAG)** with Google Gemini API.

---

## 🚀 Live Demo
## 🚀 Live Demo
👉 [Open Live App](https://ai-legal-assistant-cfpatubjmrnhsbh8jszpmx.streamlit.app/)

---

## 📌 Key Features

### 📄 Document Intelligence
- Upload PDF / DOCX / TXT files
- Automatic text extraction
- Smart chunking of documents

### 🧠 AI Chat (RAG System)
- Ask questions from your documents
- Context-aware responses using FAISS vector search
- Strict "document-only" answering mode (no hallucination)

### 📌 Legal Summarization
- Structured legal summaries
- Multiple styles: Simple / Detailed / Bullet points
- Multi-language support (English / Hindi / Hinglish)

### 🎙 Voice AI Support
- Speech-to-text input
- Voice-based interaction support

### ⚡ Performance Features
- Caching system for faster responses
- Multi-model Gemini fallback system
- Optimized vector search

---

## 🧠 Tech Stack

- Python 🐍
- Streamlit 🎈
- Google Gemini API 🤖
- FAISS (Vector Database)
- Sentence Transformers
- PyPDF / python-docx
- Pandas / NumPy

---

## 🏗️ System Architecture
User Query
↓
Streamlit UI
↓
Vector Search (FAISS)
↓
Relevant Context Retrieval
↓
Gemini LLM (RAG Prompt)
↓
Final Answer

---

## 📁 Project Structure
ai-legal-assistant/
│
├── app.py
├── requirements.txt
├── README.md
│
├── modules/
│ ├── extractor.py
│ ├── summarizer.py
│ ├── qa_chatbot.py
│ ├── vector_store.py
│ ├── ingestion.py
│ ├── embeddings.py
│ ├── cache.py
│ ├── text_splitter.py
│
├── cache_store.json
##Create Virtual Environment
python -m venv venv
venv\Scripts\activate   # Windows
##nstall Dependencies
pip install -r requirements.txt
##Create a .env file:
GEMINI_API_KEY=your_api_key_here
##Run Application
streamlit run app.py
