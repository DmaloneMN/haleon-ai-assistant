"""Unit tests for TriageAgent."""

from haleon_assistant.agents.triage_agent import TriageAgent


def test_triage_dosage_intent():
    agent = TriageAgent()
    assert agent.classify("What is the dosage?")["intent"] == "dosage"


def test_triage_general_intent():
    agent = TriageAgent()
    assert agent.classify("Tell me about Haleon products")["intent"] == "general"
