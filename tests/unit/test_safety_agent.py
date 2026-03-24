from haleon_assistant.agents.safety_agent import SafetyAgent


def test_safety_passes_on_benign_input():
    s = SafetyAgent()
    result = s.check("hello", [])
    assert result.get("ok") is True
