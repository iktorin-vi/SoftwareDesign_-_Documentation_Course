import sys
import os
import pytest
from fastapi.testclient import TestClient

# Додаємо шлях, щоб тест бачив main.py та інші модулі
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from storage.database import Base, engine

client = TestClient(app)


# Створюємо таблиці в тестовій базі перед запуском тестів
@pytest.fixture(scope="module", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    # Опціонально: можна очистити базу після тестів
    # Base.metadata.drop_all(bind=engine)


def test_messenger_integration_flow():
    # 1. Створюємо користувача A
    response_a = client.post("/users", json={"name": "Alice"})
    assert response_a.status_code == 200
    user_a_id = response_a.json()["id"]

    # 2. Створюємо користувача B
    response_b = client.post("/users", json={"name": "Bob"})
    assert response_b.status_code == 200
    user_b_id = response_b.json()["id"]

    # 3. Відправляємо повідомлення від A до B
    # Оскільки ми використовуємо BackgroundTasks, статус відразу буде 'accepted'
    msg_payload = {
        "conversationId": 101,
        "senderId": user_a_id,
        "text": "Hey Bob, check the ORM flow!"
    }
    response_msg = client.post("/messages", json=msg_payload)
    assert response_msg.status_code == 200
    assert response_msg.json()["status"] == "accepted"

    # 4. Перевіряємо історію повідомлень для розмови 101
    response_history = client.get("/conversations/101/messages")
    assert response_history.status_code == 200
    history = response_history.json()

    assert len(history) > 0
    assert history[-1]["text"] == "Hey Bob, check the ORM flow!"
    assert history[-1]["senderId"] == user_a_id
    # На момент GET запиту статус може бути вже 'delivered' через фонову задачу
    assert history[-1]["status"] in ["pending", "delivered", "accepted"]


def test_mark_as_read():
    # Перевіряємо зміну статусу на 'read' (PATCH)
    # Використовуємо id=1, припускаючи, що це перше повідомлення в базі
    response = client.patch("/messages/1/read")
    assert response.status_code == 200
    assert response.json()["new_status"] == "read"