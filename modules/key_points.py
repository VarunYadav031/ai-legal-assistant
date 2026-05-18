import re

class KeyPointsExtractor:

    def __init__(self):
        pass

    # ---------------- CLEAN TEXT ----------------
    def clean_text(self, text: str):

        # remove extra spaces
        text = re.sub(r'\s+', ' ', text)

        # remove weird symbols
        text = re.sub(r'[^\w\s.,()\-:/]', '', text)

        return text.strip()

    # ---------------- SPLIT INTO CLAUSES ----------------
    def split_clauses(self, text: str):

        # split by legal indicators
        clauses = re.split(r'\n|•|\d+\.\s', text)

        # filter short noise
        clauses = [c.strip() for c in clauses if len(c.strip()) > 40]

        return clauses

    # ---------------- EXTRACT KEY POINTS ----------------
    def extract_keypoints(self, text: str):

        text = self.clean_text(text)
        clauses = self.split_clauses(text)

        keypoints = []

        important_keywords = [
            "shall", "agree", "confidential", "terminate",
            "payment", "employee", "liability",
            "breach", "effective", "obligation"
        ]

        for clause in clauses:

            score = 0
            clause_lower = clause.lower()

            # keyword scoring
            for word in important_keywords:
                if word in clause_lower:
                    score += 1

            # length bonus (legal clauses are usually long)
            if len(clause) > 100:
                score += 1

            if score >= 2:
                keypoints.append(clause)

        # fallback: if nothing found
        if not keypoints:
            keypoints = clauses[:10]

        return keypoints


# ---------------- GLOBAL OBJECT ----------------
keypoint_extractor = KeyPointsExtractor()