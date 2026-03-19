"""Unit tests for RetrievalAgent."""

from haleon_assistant.agents.retrieval_agent import RetrievalAgent


def test_retrieval_returns_docs():
    agent = RetrievalAgent()
    docs = agent.retrieve("aspirin dose")
    assert isinstance(docs, list) and len(docs) > 0


def test_retrieval_result_has_expected_keys():
    agent = RetrievalAgent()
    results = agent.retrieve("How do I take panadol?")
    assert "title" in results[0]
    assert "url" in results[0]
    assert "snippet" in results[0]
