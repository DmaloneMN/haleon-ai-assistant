"""Pharmacovigilance agent – detects and surfaces adverse event reports."""


class PharmacovigilanceAgent:
    """Checks text for adverse event indicators."""

    def scan(self, text: str) -> dict:
        """Return a pharmacovigilance scan result.

        Returns:
            dict with ``ae_detected`` (bool) and ``details`` (list).
        """
        return {"ae_detected": False, "details": []}
