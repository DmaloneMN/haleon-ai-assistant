from haleon_assistant.agents.retrieval_agent import RetrievalAgent


def test_retrieval_returns_documents():
    r = RetrievalAgent()
    docs = r.retrieve("aspirin dose")
    assert isinstance(docs, list) and len(docs) > 0
    assert "snippet" in docs[0]
