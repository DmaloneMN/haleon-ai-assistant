"""Triage agent – classifies incoming queries to route them correctly."""


class TriageAgent:
    """Classifies a query and returns a routing dict."""

    def classify(self, query: str) -> dict:
        """Return intent dict for *query*.

        Returns ``{"intent": "dosage"}`` when dose-related keywords are present,
        otherwise ``{"intent": "general"}``.
        """
        lower = query.lower()
        if "dose" in lower or "dosage" in lower:
            return {"intent": "dosage"}
        return {"intent": "general"}
