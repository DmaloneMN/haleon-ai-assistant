"""Integration tests – end-to-end flow via the FastAPI TestClient."""

from fastapi.testclient import TestClient

from haleon_assistant.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "uptime_seconds" in data


def test_chat_endpoint_returns_answer():
    response = client.post("/api/v1/chat", json={"query": "What is the dosage for panadol?"})
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert isinstance(data["answer"], str)
    assert len(data["answer"]) > 0


def test_chat_endpoint_returns_citations():
    response = client.post("/api/v1/chat", json={"query": "Tell me about side effects"})
    assert response.status_code == 200
    data = response.json()
    assert "citations" in data
    assert isinstance(data["citations"], list)


def test_feedback_endpoint_returns_202():
    payload = {
        "query": "What is the dosage?",
        "answer": "500 mg per dose",
        "rating": 5,
        "comment": "Very helpful",
    }
    response = client.post("/api/v1/feedback", json=payload)
    assert response.status_code == 202
