from sqlalchemy.orm import Session
from database.models import Message


# Create a new message
def create_message(db: Session, chat_id: int, user_id: int, content: str):
    message = Message(chat_id=chat_id, user_id=user_id, message=content)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


# Retrieve all messages for a chat
def get_messages_by_chat(db: Session, chat_id: int):
    return db.query(Message).filter(Message.chat_id == chat_id).all()


# Retrieve a specific message by ID
def get_message_by_id(db: Session, message_id: int):
    return db.query(Message).filter(Message.id == message_id).first()


# Update a message's content
def update_message_content(db: Session, message_id: int, new_content: str):
    message = db.query(Message).filter(Message.id == message_id).first()
    if message:
        message.message = new_content
        db.commit()
        db.refresh(message)
    return message


# Delete a message
def delete_message(db: Session, message_id: int):
    message = db.query(Message).filter(Message.id == message_id).first()
    if message:
        db.delete(message)
        db.commit()
    return message


async def update_message_response(db: Session, message_id: int, response_text: str):
    msg = db.query(Message).filter(Message.id == message_id).first()
    print(f"updating the message #{msg.id} with response ", response_text)
    if msg:
        msg.response = response_text
        db.commit()
        db.refresh(msg)
    return msg