"""Tests for the /chat endpoint."""


def test_chat_endpoint_returns_response(client):
    response = client.post(
        "/chat/",
        json={"message": "What is the dosage for Panadol?"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert isinstance(data["answer"], str)
    assert len(data["answer"]) > 0


def test_chat_blocked_message(client):
    """A very long (but benign) message should still return 200."""
    long_message = "Tell me about Panadol. " * 50
    response = client.post("/chat/", json={"message": long_message})
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
