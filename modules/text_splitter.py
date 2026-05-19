import re
import math


class TextSplitter:

    def __init__(self, chunk_size=800, overlap=150):
        self.chunk_size = chunk_size
        self.overlap = overlap

    # ---------------- CLEAN TEXT ----------------
    def clean_text(self, text: str) -> str:
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    # ---------------- SMART SPLIT ----------------
    def split_text(self, text: str):

        text = self.clean_text(text)

        # STEP 1: split by sentences (IMPORTANT FIX)
        sentences = re.split(r'(?<=[.!?]) +', text)

        chunks = []
        current_chunk = ""

        for sentence in sentences:

            # if adding sentence exceeds limit → save chunk
            if len(current_chunk) + len(sentence) > self.chunk_size:

                if current_chunk:
                    chunks.append(current_chunk.strip())

                # overlap logic (keep last part)
                overlap_text = current_chunk[-self.overlap:] if self.overlap > 0 else ""
                current_chunk = overlap_text + " " + sentence

            else:
                current_chunk += " " + sentence

        # last chunk
        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        # remove very small junk chunks
        final_chunks = [c for c in chunks if len(c) > 50]

        return final_chunks


# ---------------- GLOBAL INSTANCE ----------------
text_splitter = TextSplitter()