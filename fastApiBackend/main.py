from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from database.db_connection import Base, engine, get_db
import database.models
from utilites.auth.dependencies import get_current_user
# Routers:
from API.auth import router as auth_router
from API.chat import router as chat_router



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router, tags=["Authentication"])
app.include_router(chat_router, tags=["Chat"])

# Initialize tables
Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Hello there"}

# This api just to check if I am handling auth correctly, will be removed
@app.get("/profile")
def get_user_profile(current_user: database.models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Protected route that returns the profile of the current user.
    Requires a valid JWT in the Authorization header.
    """
    return {
        "user_id": current_user.id,
        "username": current_user.username,
        "created_at": current_user.created_at
    }
