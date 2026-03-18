"""Unit tests for TriageAgent."""

from haleon_assistant.agents.triage_agent import TriageAgent


def test_triage_dosage_route():
    agent = TriageAgent()
    assert agent.classify("What is the dosage for paracetamol?") == "dosage"


def test_triage_side_effects_route():
    agent = TriageAgent()
    assert agent.classify("What are the side effects of ibuprofen?") == "side_effects"


def test_triage_pharmacovigilance_route():
    agent = TriageAgent()
    assert agent.classify("I want to report an adverse reaction") == "pharmacovigilance"


def test_triage_general_route():
    agent = TriageAgent()
    assert agent.classify("Tell me about Haleon products") == "general"
