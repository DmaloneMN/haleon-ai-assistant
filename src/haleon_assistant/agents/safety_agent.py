"""Safety agent – quick PII and toxicity checks.

TODO: replace stubs with real Azure Content Safety API calls.
"""


class SafetyAgent:
    """Runs lightweight safety checks on a query before it is processed."""

    def check(self, text: str) -> dict:
        """Return a result dict with key ``pass`` (bool) and ``reason`` (str).

        Current stub: always passes unless the word "UNSAFE" appears in text
        (useful for testing the rejection path without real safety services).
        """
        # TODO: call Azure Content Safety API for PII detection and toxicity scoring
        if "UNSAFE" in text:
            return {"pass": False, "reason": "Simulated safety failure (test trigger)."}
        return {"pass": True, "reason": "ok"}
