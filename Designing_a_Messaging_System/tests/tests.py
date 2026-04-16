import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)


def test_full_messenger_flow():
    # 1. Create user A
    response_a = client.post("/users", json={"name": "Alice"})
    assert response_a.status_code == 200
    user_a_id = response_a.json()["id"]

    # 2. Create user B
    response_b = client.post("/users", json={"name": "Bob"})
    assert response_b.status_code == 200
    user_b_id = response_b.json()["id"]

    # 3. Send a message from A to B (у спільний conversationId = 1)
    msg_payload = {
        "conversationId": 1,
        "senderId": user_a_id,
        "text": "Hello Bob!"
    }
    response_msg = client.post("/messages", json=msg_payload)
    assert response_msg.status_code == 200
    assert response_msg.json()["status"] == "pending"

    # 4. Retrieve message history
    response_history = client.get("/conversations/1/messages")
    assert response_history.status_code == 200

    # 5. Verify that the message exists
    history = response_history.json()
    assert len(history) > 0
    assert history[-1]["text"] == "Hello Bob!"
    assert history[-1]["senderId"] == user_a_id