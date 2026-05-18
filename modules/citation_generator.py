# modules/citation_generator.py

import re


class CitationGenerator:
    def __init__(self):
        pass

    def _clean_text(self, text: str) -> str:
        return re.sub(r"\s+", " ", text).strip()

    def _tokenize(self, text: str):
        # Keep words with length >= 4 and remove common stopwords
        stopwords = {
            "this", "that", "with", "from", "have", "shall",
            "under", "agreement", "company", "employee",
            "their", "there", "which", "these", "those"
        }

        words = re.findall(r"\w+", text.lower())

        return {
            word
            for word in words
            if len(word) >= 4 and word not in stopwords
        }

    def _extract_keyword_snippet(
        self,
        chunk: str,
        priority_keywords=None,
        window: int = 300
    ) -> str:
        """
        Extract snippet around priority keywords such as:
        employee, termination, confidential, payment, salary.
        """

        chunk_clean = self._clean_text(chunk)
        chunk_lower = chunk_clean.lower()

        if priority_keywords is None:
            priority_keywords = []

        # Search priority keywords first
        for keyword in priority_keywords:
            idx = chunk_lower.find(keyword.lower())
            if idx != -1:
                start = max(0, idx - 80)
                end = min(len(chunk_clean), idx + window)

                snippet = chunk_clean[start:end]

                if start > 0:
                    snippet = "..." + snippet
                if end < len(chunk_clean):
                    snippet += "..."

                return snippet

        # Fallback
        return chunk_clean[:300] + ("..." if len(chunk_clean) > 300 else "")

    def generate_citation(self, answer: str, source_chunks: list):
        if not source_chunks:
            return {
                "citation": "No source found.",
                "confidence": "Low"
            }

        answer_words = self._tokenize(answer)

        # Priority legal keywords
        priority_keywords = [
            "employee",
            "termination",
            "terminate",
            "confidential",
            "confidentiality",
            "payment",
            "salary",
            "breach",
            "obligation",
            "duty",
            "duties",
            "agreement"
        ]

        best_chunk = ""
        best_score = -1

        for chunk in source_chunks:
            if not chunk:
                continue

            chunk_words = self._tokenize(chunk)
            score = len(answer_words.intersection(chunk_words))

            # Boost score if chunk contains priority keywords
            chunk_lower = chunk.lower()
            for keyword in priority_keywords:
                if keyword in chunk_lower:
                    score += 2

            if score > best_score:
                best_score = score
                best_chunk = chunk

        # Confidence scoring
        if best_score >= 10:
            confidence = "High"
        elif best_score >= 4:
            confidence = "Medium"
        else:
            confidence = "Low"

        # Extract focused snippet
        citation = self._extract_keyword_snippet(
            best_chunk,
            priority_keywords=priority_keywords
        )

        return {
            "citation": citation,
            "confidence": confidence
        }


# Global object
citation_generator = CitationGenerator()