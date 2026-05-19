from modules.text_splitter import text_splitter
from modules.vector_store import vs


def ingest_document(text: str):
    """
    Convert raw document into chunks and store in vector DB
    """

    if not text or len(text.strip()) < 50:
        return 0

    try:
        # ---------------- STEP 1: SPLIT TEXT ----------------
        chunks = text_splitter.split_text(text)

        if not chunks:
            return 0

        # ---------------- STEP 2: CLEAN CHUNKS ----------------
        clean_chunks = []
        for c in chunks:
            c = c.strip()
            if len(c) > 20:   # ignore noise
                clean_chunks.append(c)

        if not clean_chunks:
            return 0

        # ---------------- STEP 3: STORE IN VECTOR DB ----------------
        vs.add(clean_chunks)

        return len(clean_chunks)

    except Exception as e:
        print("Ingestion Error:", e)
        return 0