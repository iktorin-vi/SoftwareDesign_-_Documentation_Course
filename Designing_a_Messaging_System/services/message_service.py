from sqlalchemy.orm import Session
from models.database_models import User, Message
from datetime import datetime

class MessageService:
    @staticmethod
    def create_user(db: Session, name: str):
        db_user = User(name=name)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user.id

    @staticmethod
    def send_message(db: Session, conv_id: int, sender_id: int, text: str):
        new_msg = Message(conversationId=conv_id, senderId=sender_id, text=text)
        db.add(new_msg)
        db.commit()
        db.refresh(new_msg)
        return new_msg.id

    @staticmethod
    def get_history(db: Session, conv_id: int):
        return db.query(Message).filter(Message.conversationId == conv_id).all()

    @staticmethod
    def update_status(db: Session, message_id: int, status: str):
        msg = db.query(Message).filter(Message.id == message_id).first()
        if msg:
            msg.status = status
            if status == "delivered": msg.deliveredAt = datetime.utcnow()
            if status == "read": msg.readAt = datetime.utcnow()
            db.commit()