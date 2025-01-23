from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database.db_connection import Base, engine, get_db
import database.models
from API.auth import router as auth_router
from utilites.auth.dependencies import get_current_user


app = FastAPI()

app.include_router(auth_router, tags=["Authentication"])

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
