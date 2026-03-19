"""Safety agent – quick PII and toxicity checks."""


class SafetyAgent:
    """Runs lightweight safety checks on a query before it is processed."""

    def check(self, query: str, docs: list) -> dict:
        """Return a result dict with key ``ok`` (bool) and ``issues`` (list).

        Current stub: always passes (scaffold placeholder).
        """
        return {"ok": True, "issues": []}
