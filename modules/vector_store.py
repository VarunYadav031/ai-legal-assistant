import chromadb
from modules.embeddings import get_embedding
import hashlib
import streamlit as st


class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="chroma_db")
        self.collection = self.client.get_or_create_collection(
            name="legal_docs"
        )

    def get_id(self, text):
        return hashlib.md5(text.encode()).hexdigest()

    def add_documents(self, texts):
        if isinstance(texts, str):
            texts = [texts]

        for text in texts:
            doc_id = self.get_id(text)

            existing = self.collection.get(ids=[doc_id])
            if existing and existing.get("ids"):
                continue

            emb = get_embedding(text)

            self.collection.add(
                documents=[text],
                embeddings=[emb],
                ids=[doc_id]
            )

    def search(self, query, n_results=2):
        query_emb = get_embedding(query)

        results = self.collection.query(
            query_embeddings=[query_emb],
            n_results=n_results
        )

        return results.get("documents", [[]])[0]


# ✅ IMPORTANT: cache full vector store (BIG SPEED BOOST)
@st.cache_resource
def get_vector_store():
    return VectorStore()


vs = get_vector_store()