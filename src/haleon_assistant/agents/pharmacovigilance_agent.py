class PharmacovigilanceAgent:
    """Stub pharmacovigilance scanner."""

    def scan(self, text: str) -> dict:
        # No adverse events detected in scaffold
        return {"ae_detected": False, "details": []}
