"""Unit tests for RetrievalAgent."""

from haleon_assistant.agents.retrieval_agent import RetrievalAgent


def test_retrieval_returns_non_empty_list():
    agent = RetrievalAgent()
    results = agent.retrieve("What is the recommended dosage?")
    assert isinstance(results, list)
    assert len(results) > 0


def test_retrieval_result_has_expected_keys():
    agent = RetrievalAgent()
    results = agent.retrieve("How do I take panadol?", route="dosage")
    assert "id" in results[0]
    assert "title" in results[0]
    assert "excerpt" in results[0]
