"""Tests for the /feedback endpoint."""


def test_feedback_accepted(client):
    response = client.post(
        "/feedback/",
        json={
            "session_id": "sess-001",
            "message_id": "msg-abc",
            "rating": 1,
            "comment": "Very helpful!",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "accepted"
    assert data["message_id"] == "msg-abc"
