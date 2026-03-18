"""Triage agent – classifies incoming queries to route them correctly.

TODO: replace stub with a real LLM-based intent classifier.
"""


class TriageAgent:
    """Classifies a query and returns a routing label."""

    # Known routes
    ROUTES = ("dosage", "side_effects", "pharmacovigilance", "general")

    def classify(self, query: str) -> str:
        """Return a route string for *query*.

        Current stub: keyword-based classification; replace with LLM call.
        """
        q = query.lower()
        # Check pharmacovigilance first (has overlapping terms with side_effects)
        if any(w in q for w in ("report", "pharmacovigilance", "pv")):
            return "pharmacovigilance"
        if any(w in q for w in ("dose", "dosage", "how much", "mg")):
            return "dosage"
        if any(w in q for w in ("side effect", "adverse", "reaction")):
            return "side_effects"
        return "general"
