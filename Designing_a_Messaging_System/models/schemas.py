from pydantic import BaseModel
from typing import Optional

# Модель для створення користувача
class UserSchema(BaseModel):
    name: str

# Модель для відправки повідомлення

class MessageSchema(BaseModel):
    conversationId: int
    senderId: int
    text: str

# Модель для відповіді (Response)
class MessageResponse(BaseModel):
    id: int
    conversationId: int
    senderId: int
    text: str
    status: str
    createdAt: str