"""Red-team placeholder – jailbreak tests.

These tests are marked xfail until adversarial evaluation is implemented.
TODO: replace with automated jailbreak probing using a red-team LLM.
"""

import pytest


@pytest.mark.xfail(reason="Jailbreak evaluation not yet implemented", strict=False)
def test_prompt_injection_rejected():
    """Assert the assistant ignores prompt-injection attempts."""
    # TODO: send adversarial prompts and verify they are rejected
    assert False, "Not implemented"


@pytest.mark.xfail(reason="Jailbreak evaluation not yet implemented", strict=False)
def test_system_prompt_not_leaked():
    """Assert the system prompt is not returned to the user."""
    # TODO: probe for system prompt leakage
    assert False, "Not implemented"
