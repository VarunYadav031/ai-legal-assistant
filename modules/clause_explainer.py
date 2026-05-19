import re


class ClauseExplainer:

    def __init__(self):
        pass

    # ---------------- CLEAN CLAUSE ----------------
    def clean_clause(self, text: str):
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    # ---------------- EXPLAIN CLAUSE ----------------
    def explain_clause(self, clause: str):

        clause = self.clean_clause(clause)
        lower = clause.lower()

        # ---------------- CONFIDENTIALITY ----------------
        if "confidential" in lower:
            return {
                "original": clause,
                "simple": "You are not allowed to share company secrets or private information with anyone.",
                "category": "Confidentiality"
            }

        # ---------------- TERMINATION ----------------
        if "terminate" in lower or "termination" in lower:
            return {
                "original": clause,
                "simple": "This explains when and how the agreement can be ended.",
                "category": "Termination"
            }

        # ---------------- PAYMENT ----------------
        if "payment" in lower or "salary" in lower:
            return {
                "original": clause,
                "simple": "This clause describes payment terms, salary or financial conditions.",
                "category": "Payment"
            }

        # ---------------- EMPLOYEE ----------------
        if "employee" in lower or "obligation" in lower:
            return {
                "original": clause,
                "simple": "This describes what the employee must do under the agreement.",
                "category": "Obligation"
            }

        # ---------------- BREACH ----------------
        if "breach" in lower:
            return {
                "original": clause,
                "simple": "This explains what happens if rules are broken.",
                "category": "Breach"
            }

        # ---------------- DEFAULT ----------------
        return {
            "original": clause,
            "simple": "This is a legal clause explained in simple language.",
            "category": "General"
        }


# ---------------- GLOBAL OBJECT ----------------
clause_explainer = ClauseExplainer()