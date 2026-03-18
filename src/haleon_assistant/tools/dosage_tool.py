"""Dosage tool – looks up dosage information for a product.

TODO: replace lookup table with a real database / Azure AI Search query.
"""

# Example lookup table – expand with real product data
_DOSAGE_DATA: dict = {
    "panadol": {
        "adult": "500 mg – 1000 mg every 4–6 hours (max 4000 mg/day)",
        "child": "10–15 mg/kg every 4–6 hours as directed",
    },
    "voltarol": {
        "adult": "50 mg two or three times daily",
        "child": "Not recommended under 14 years without medical advice",
    },
}


class DosageTool:
    """Returns dosage information for a given product identifier."""

    def lookup(self, product_id: str) -> dict:
        """Return dosage dict for *product_id* (case-insensitive).

        Returns an empty dict if the product is not found in the lookup table.
        """
        # TODO: query real product monograph database
        return _DOSAGE_DATA.get(product_id.lower(), {})
