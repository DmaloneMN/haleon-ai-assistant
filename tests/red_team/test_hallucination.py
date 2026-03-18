"""Red-team placeholder – hallucination tests.

These tests are marked xfail until real LLM evaluation is implemented.
TODO: replace with automated hallucination detection using a judge model.
"""

import pytest


@pytest.mark.xfail(reason="Hallucination detection not yet implemented", strict=False)
def test_no_hallucination_on_dosage_query():
    """Assert the model does not invent dosage information."""
    # TODO: call the real LLM endpoint and evaluate answer factuality
    assert False, "Not implemented"


@pytest.mark.xfail(reason="Hallucination detection not yet implemented", strict=False)
def test_no_fabricated_citations():
    """Assert all returned citation IDs refer to real documents."""
    # TODO: cross-check returned citations against the search index
    assert False, "Not implemented"
