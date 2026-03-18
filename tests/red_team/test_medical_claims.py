"""Red-team placeholder – medical claims tests.

These tests are marked xfail until medical accuracy evaluation is implemented.
TODO: replace with automated claims-checking using a medical knowledge base.
"""

import pytest


@pytest.mark.xfail(reason="Medical claims evaluation not yet implemented", strict=False)
def test_no_unsupported_medical_claims():
    """Assert the assistant does not make unsupported medical claims."""
    # TODO: evaluate answers against approved product information leaflets
    assert False, "Not implemented"


@pytest.mark.xfail(reason="Medical claims evaluation not yet implemented", strict=False)
def test_recommends_professional_consultation():
    """Assert the assistant recommends consulting a professional when appropriate."""
    # TODO: check that answers to clinical questions include the consultation disclaimer
    assert False, "Not implemented"
