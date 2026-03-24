from haleon_assistant.agents.triage_agent import TriageAgent


def test_triage_detects_dosage_intent():
    t = TriageAgent()
    out = t.classify("What is the dosage?")
    assert out.get("intent") == "dosage"
