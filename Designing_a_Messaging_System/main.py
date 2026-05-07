import time
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List

# Імпортуємо наші модулі
from storage.database import engine, Base, get_db
from models.database_models import User, Message
from models.schemas import UserSchema, MessageSchema
from services.message_service import MessageService

# Створюємо таблиці в базі даних (якщо їх ще немає)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Messenger API (Advanced)",
    description="Lab 2: Implementation with ORM, DI, and Background Message Queue",
    version="2.0.0"
)


# --- WORKER (Імітація черги повідомлень) ---
def process_delivery_queue(message_id: int, db_session_factory):
    """
    Ця функція імітує роботу фонового брокера повідомлень.
    Вона отримує id повідомлення і намагається змінити його статус.
    """
    print(f"🚀 [Queue] Processing delivery for message ID: {message_id}...")

    # Створюємо нову сесію для фонового завдання
    db = next(db_session_factory())
    try:
        # Імітуємо затримку мережі (ніби повідомлення летить до отримувача)
        time.sleep(2)
        MessageService.update_status(db, message_id, "delivered")
        print(f"✅ [Queue] Message {message_id} status updated to 'delivered'")
    except Exception as e:
        print(f"❌ [Queue] Failed to process message {message_id}: {e}")
    finally:
        db.close()


# --- ROUTES (Маршрути API) ---

@app.get("/")
def root():
    return {"status": "online", "message": "Messenger API is running"}


# 1. Створення користувача
@app.post("/users", response_model=None)
def create_user(user: UserSchema, db: Session = Depends(get_db)):
    """Creates a new user in the system."""
    uid = MessageService.create_user(db, user.name)
    return {"id": uid, "name": user.name}


# 2. Відправка повідомлення (з використанням черги)
@app.post("/messages")
def send_message(
        msg: MessageSchema,
        background_tasks: BackgroundTasks,
        db: Session = Depends(get_db)
):
    """
    Sends a message.
    The message is first saved to DB (Persistence),
    then added to the Background Task queue (Message Queue logic).
    """
    # Збереження в БД (Статус за замовчуванням 'pending')
    mid = MessageService.send_message(db, msg.conversationId, msg.senderId, msg.text)

    # Додавання в "чергу" на фонову обробку
    background_tasks.add_task(process_delivery_queue, mid, get_db)

    return {
        "messageId": mid,
        "status": "accepted",
        "detail": "Message is queued for delivery"
    }


# 3. Отримання історії повідомлень (GET)
@app.get("/conversations/{id}/messages")
def get_messages(id: int, db: Session = Depends(get_db)):
    """Retrieves all messages for a specific conversation (User 'comes online')."""
    messages = MessageService.get_history(db, id)
    if not messages:
        return []
    return messages


# 4. Оновлення статусу на 'read' (PATCH)
@app.patch("/messages/{id}/read")
def mark_as_read(id: int, db: Session = Depends(get_db)):
    """Manually updates message status to 'read'."""
    MessageService.update_status(db, id, "read")
    return {"status": "success", "message_id": id, "new_status": "read"}


# 5. Видалення користувача (опціонально)
@app.delete("/users/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": "User deleted"}