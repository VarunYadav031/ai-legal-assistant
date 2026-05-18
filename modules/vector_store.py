import chromadb
import hashlib
from modules.embeddings import get_embedding


class VectorStore:
    def __init__(self):
        # ⚡ persistent DB (loaded once)
        self.client = chromadb.PersistentClient(path="chroma_db")
        self.collection = self.client.get_or_create_collection(
            name="legal_docs"
        )

    # ---------------- ID GENERATION ----------------
    def make_id(self, text):
        return hashlib.md5(text.encode()).hexdigest()

    # ---------------- FAST INSERT (NO DUPLICATES) ----------------
    def add_documents(self, texts):
        if isinstance(texts, str):
            texts = [texts]

        for text in texts:
            doc_id = self.make_id(text)

            # ⚡ skip if already exists (VERY IMPORTANT)
            existing = self.collection.get(ids=[doc_id])
            if existing and existing.get("ids"):
                continue

            emb = get_embedding(text)

            self.collection.add(
                documents=[text],
                embeddings=[emb],
                ids=[doc_id]
            )

    # ---------------- FAST SEARCH ----------------
    def search(self, query, n_results=4):
        query_emb = get_embedding(query)

        results = self.collection.query(
            query_embeddings=[query_emb],
            n_results=n_results,
            include=["documents"]
        )

        return results["documents"][0] if results["documents"] else []


# global instance (created once)
vs = VectorStore()