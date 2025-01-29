from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from database.models import Chat


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


def is_chat_owned_by_user(user_id: int, chat_id: int, db: Session) -> bool:
    """
    Check if a chat belongs to a user.

    Args:
        user_id (int): The ID of the user.
        chat_id (int): The ID of the chat.
        db (Session): SQLAlchemy database session.

    Returns:
        bool: True if the chat belongs to the user, False otherwise.
    """
    try:
        print(f"chat with chat id = {chat_id} is accessed by user {user_id} ")
        chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == user_id).one_or_none()
        return chat is not None
    except NoResultFound:

        return False
    except Exception as e:
        # Log or handle unexpected exceptions
        print(f"An error occurred: {e}")
        return False