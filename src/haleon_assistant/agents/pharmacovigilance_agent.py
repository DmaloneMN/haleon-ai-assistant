"""Pharmacovigilance agent – detects and surfaces adverse event reports.

TODO: integrate with the real PV database / regulatory submission pipeline.
"""


class PharmacovigilanceAgent:
    """Checks a query for adverse event indicators and returns a report."""

    def check(self, query: str) -> dict:
        """Return a pharmacovigilance assessment for *query*.

        Returns:
            dict with ``adverse_events`` (list) – empty in this stub – and
            ``action_required`` (bool).
        """
        # TODO: parse query for adverse event signals; flag for medical review
        return {"adverse_events": [], "action_required": False}
