from fastapi import FastAPI
from database.db_connection import Base, engine
from database.models import User, Chat, Message

app = FastAPI()

# Initialize tables
Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Hello there"}

