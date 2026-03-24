from haleon_assistant.agents.safety_agent import SafetyAgent


def test_safety_passes_on_benign_input():
    s = SafetyAgent()
    result = s.check("hello", [])
    assert result.get("ok") is True


def test_safety_flags_empty_input():
    s = SafetyAgent()
    # content_safety_tool flags empty text as unsafe in scaffold
    result = s.check("", [])
    assert result.get("ok") is False
