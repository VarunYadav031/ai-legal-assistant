from sentence_transformers import SentenceTransformer
import numpy as np
from functools import lru_cache

# ✅ Load model ONCE (IMPORTANT FOR STREAMLIT STABILITY)
model = SentenceTransformer("all-MiniLM-L6-v2")


# ---------------- CACHE EMBEDDINGS ----------------
@lru_cache(maxsize=1000)
def _cached_encode(text: str):
    """
    Internal cached encoder to avoid repeated computation
    """
    return model.encode(text)


# ---------------- MAIN FUNCTION ----------------
def get_embedding(text: str):
    """
    Convert text into vector embedding (safe + optimized)
    """

    if not text or not isinstance(text, str):
        return [0.0] * 384  # fallback vector size for MiniLM

    try:
        vector = _cached_encode(text)

        # ensure numpy compatibility
        return np.array(vector, dtype="float32").tolist()

    except Exception as e:
        print("Embedding error:", str(e))

        # fallback safe vector
        return [0.0] * 384