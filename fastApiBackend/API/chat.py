import json
from utilites.alchemy_encoder import AlchemyEncoder
from fastapi import APIRouter, Depends, HTTPException
from sse_starlette.sse import EventSourceResponse
from sqlalchemy.orm import Session
from database.db_connection import get_db
from database.models import Chat, Message, User
from database.operations.chat_crud import create_chat, is_chat_owned_by_user
from database.operations.message_crud import create_message, update_message_response
from graph.graph_compilation import app as graph_app
from utilites.auth.dependencies import get_current_user
from pydantic import BaseModel
router = APIRouter()

@router.post("/chats", response_model=dict)
def create_chat_logic(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Create a new chat for the given user.
    """
    prev_chats_number = db.query(Chat).filter(Chat.user_id == current_user.id).count()
    new_chat = create_chat(db, title=f"New Chat {prev_chats_number}", user_id=current_user.id)
    return {"chat_id": new_chat.id, "message": "Chat created"}


@router.post("/chats/{chat_id}/message")
async def create_message_with_json_response(chat_id: int,
                         user_message: str,
                         current_user: User = Depends(get_current_user),
                         db: Session = Depends(get_db)):
    """
    1. Store user's message in the DB.
    2. Generate the LLM response.
    3. Store and return the final response in JSON.
    """

    chat = db.query(Chat).filter_by(id=chat_id, user_id=current_user.id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found or not yours")

    db_msg = create_message(db, chat_id=chat_id, user_id=current_user.id, content=user_message)

    # Generate the full LLM response
    final_response = []
    inputs = {"question": user_message}
    for output in graph_app.stream(inputs):
        for node_name, node_data in output.items():
            chunk = node_data.get("generation")
            if chunk:
                final_response.append(chunk)

    combined_response = "".join(final_response)

    # Store in DB
    updated_message = await update_message_response(db, db_msg.id, combined_response)

    return json.dumps(updated_message, cls=AlchemyEncoder)



@router.post("/chats/{chat_id}/messages/stream")
async def create_message_and_stream_response(chat_id: int,
                                             user_message: str,
                                             current_user: User = Depends(get_current_user),
                                             db: Session = Depends(get_db)):
    """
    1. Store user's message in the DB.
    2. Stream the LLM response chunk by chunk (SSE).
    3. Store the final response in the DB.
    """
    print(f"Received message: {user_message}")
    chat = db.query(Chat).filter_by(id=chat_id, user_id=current_user.id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found or not yours")

    db_msg = create_message(db, chat_id=chat_id, user_id=current_user.id, content=user_message)

    async def event_generator():
        final_response = []
        inputs = {"question": user_message}

        for output in graph_app.stream(inputs):
            for node_name, node_data in output.items():
                # TODO, make this real chunks, now I am sending the woe generation as one
                chunk = node_data.get("generation")
                print("chunk ", chunk)
                if chunk:
                    final_response.append(chunk)

        # Once done, store the final combined response in DB
        combined_response = "".join(final_response)
        updated_message = await update_message_response(db, db_msg.id, combined_response)

        yield {"event": "end", "data": json.dumps(updated_message, cls=AlchemyEncoder)}

    return EventSourceResponse(event_generator(), media_type="application/json")


@router.get("/chats/{chat_id}")
async def get_chat_messages(chat_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    chat = is_chat_owned_by_user(current_user.id, chat_id, db)
    if not chat:
        raise HTTPException(401)

    messages = db.query(Message).filter_by(chat_id=chat_id).all()
    return json.dumps(messages, cls=AlchemyEncoder)
