from sqlalchemy.orm import Session
from database.models import Chat, Message


# Create a new chat
def create_chat(db: Session, user_id: int, title: str):
    chat = Chat(user_id=user_id, title=title)
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat


# Retrieve all chats for a user
def get_chats_by_user(db: Session, user_id: int):
    return db.query(Chat).filter(Chat.user_id == user_id).all()


# Retrieve a specific chat by ID
def get_chat_by_id(db: Session, chat_id: int):
    return db.query(Chat).filter(Chat.id == chat_id).first()


# Update chat title
def update_chat_title(db: Session, chat_id: int, new_title: str):
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if chat:
        chat.title = new_title
        db.commit()
        db.refresh(chat)
    return chat


# Delete a chat
def delete_chat(db: Session, chat_id: int):
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if chat:
        db.delete(chat)
        db.commit()
    return chat
