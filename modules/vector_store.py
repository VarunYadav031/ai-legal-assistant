import faiss
import numpy as np
from modules.embeddings import get_embedding


class VectorStore:

    def __init__(self):
        self.docs = []
        self.embeddings = []
        self.index = None

    # ---------------- ADD DOCUMENTS (SAFE + CLEAN) ----------------
    def add(self, chunks):

        if not chunks:
            return

        for chunk in chunks:
            try:
                emb = get_embedding(chunk)

                if emb is None or len(emb) == 0:
                    continue

                self.docs.append(chunk)
                self.embeddings.append(emb)

            except Exception as e:
                print("Embedding error in vector store:", e)
                continue

        self._build_index()

    # ---------------- BUILD INDEX (SAFE + RESET FIX) ----------------
    def _build_index(self):

        if len(self.embeddings) == 0:
            return

        try:
            vectors = np.array(self.embeddings).astype("float32")

            if len(vectors.shape) != 2:
                print("Invalid embedding shape:", vectors.shape)
                return

            dim = vectors.shape[1]

            # 🔥 IMPORTANT FIX: reset index before rebuild
            self.index = faiss.IndexFlatL2(dim)

            # normalize vectors for better semantic search
            faiss.normalize_L2(vectors)

            self.index.add(vectors)

        except Exception as e:
            print("FAISS build error:", e)
            self.index = None

    # ---------------- SEARCH (IMPROVED + SAFE) ----------------
    def search(self, query, n_results=5):

        if not query or not isinstance(query, str):
            return []

        if self.index is None or len(self.docs) == 0:
            return []

        try:
            query_vec = np.array(get_embedding(query)).astype("float32").reshape(1, -1)

            # normalize query vector (IMPORTANT FIX)
            faiss.normalize_L2(query_vec)

            distances, indices = self.index.search(query_vec, n_results)

            results = []

            for i in indices[0]:
                if 0 <= i < len(self.docs):
                    results.append(self.docs[i])

            return results

        except Exception as e:
            print("Vector search error:", e)
            return []


# ---------------- GLOBAL INSTANCE ----------------
vs = VectorStore()