"""Unit tests for SafetyAgent."""

from haleon_assistant.agents.safety_agent import SafetyAgent


def test_safety_passes_benign_input():
    agent = SafetyAgent()
    result = agent.check("What is the recommended dose for adults?")
    assert result["pass"] is True


def test_safety_fails_on_trigger_word():
    agent = SafetyAgent()
    result = agent.check("This is UNSAFE content")
    assert result["pass"] is False
    assert "reason" in result
