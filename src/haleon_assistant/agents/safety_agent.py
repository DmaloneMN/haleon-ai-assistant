class SafetyAgent:
    """Simple scaffold safety agent; always returns ok=True in this scaffold."""

    def check(self, query: str, docs: list) -> dict:
        # Real checks (PII, toxicity, medical risk) should be implemented later.
        return {"ok": True, "issues": []}
