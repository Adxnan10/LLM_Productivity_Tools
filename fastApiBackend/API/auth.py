from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database.models import User
from database.db_connection import get_db
from utilites.auth.hashing import hash_password, verify_password
from utilites.auth.jwt_handling import create_access_token

router = APIRouter()


@router.post("/register")
def register_user(username: str, password: str, db: Session = Depends(get_db)):
    # Check if username already exists
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Hash the password before storing it
    hashed_password = hash_password(password)

    # Create new user
    new_user = User(username=username, password_hash=hashed_password)
    db.add(new_user)
    db.commit()

    # Generate JWT token after registration
    access_token = create_access_token(data={"sub": new_user.username, "user_id": new_user.id})

    return {"message": "User registered successfully", "user_id": new_user.id, "access_token": access_token}


@router.post("/login")
def login_user(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    # Extract username and password from form_data
    username = form_data.username
    password = form_data.password

    # Check user in database
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # Create token
    access_token = create_access_token(data={"sub": username, "user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
