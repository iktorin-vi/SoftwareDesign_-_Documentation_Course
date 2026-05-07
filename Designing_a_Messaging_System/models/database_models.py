from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from storage.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    conversationId = Column(Integer)
    senderId = Column(Integer)
    text = Column(String)
    status = Column(String, default="pending")
    createdAt = Column(DateTime, default=datetime.utcnow)
    deliveredAt = Column(DateTime, nullable=True)
    readAt = Column(DateTime, nullable=True)