import chromadb
from modules.embeddings import get_embedding

class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="chroma_db")
        self.collection = self.client.get_or_create_collection(
            name="legal_docs"
        )

    def add_documents(self, texts):
        for i, text in enumerate(texts):
            emb = get_embedding(text)

            self.collection.add(
                documents=[text],
                embeddings=[emb],
                ids=[f"doc_{len(texts)}_{i}"]
            )

    def search(self, query, n_results=4):
        query_emb = get_embedding(query)

        results = self.collection.query(
            query_embeddings=[query_emb],
            n_results=n_results
        )

        return results["documents"][0] if results["documents"] else []


# global instance
vs = VectorStore()