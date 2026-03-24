class TriageAgent:
    """Minimal intent classifier for scaffold/testing purposes."""

    def classify(self, query: str) -> dict:
        if not query:
            return {"intent": "general"}
        lower = query.lower()
        if "dose" in lower or "dosage" in lower:
            return {"intent": "dosage"}
        if "adverse" in lower or "reaction" in lower:
            return {"intent": "pharmacovigilance"}
        return {"intent": "general"}
