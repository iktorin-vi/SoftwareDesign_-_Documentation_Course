from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from services.message_service import MessageService
from storage.database import init_db

app = FastAPI(title="Messenger")
init_db()

class UserSchema(BaseModel): name: str
class MessageSchema(BaseModel):
    conversationId: int
    senderId: int
    text: str

@app.post("/users")
def create_user(user: UserSchema):
    return {"id": MessageService.create_user(user.name)}

@app.post("/messages")
def send_message(msg: MessageSchema):
    mid = MessageService.send_message(msg.conversationId, msg.senderId, msg.text)
    if not mid: raise HTTPException(status_code=400, detail="Invalid message")
    return {"messageId": mid, "status": "pending"}

@app.get("/conversations/{id}/messages")
def get_messages(id: int):
    return MessageService.get_history(id)

@app.patch("/messages/{id}/delivered")
def set_delivered(id: int):
    MessageService.mark_as_delivered(id)
    return {"status": "success", "message": "Marked as delivered"}

@app.patch("/messages/{id}/read")
def set_read(id: int):
    MessageService.mark_as_read(id)
    return {"status": "success", "message": "Marked as read"}