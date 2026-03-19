"""Unit tests for SafetyAgent."""

from haleon_assistant.agents.safety_agent import SafetyAgent


def test_safety_passes_benign_input():
    agent = SafetyAgent()
    result = agent.check("What is the recommended dose for adults?", [])
    assert result.get("ok") is True


def test_safety_result_has_issues_key():
    agent = SafetyAgent()
    result = agent.check("hello", [])
    assert "issues" in result
