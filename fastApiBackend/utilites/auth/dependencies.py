from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from database.db_connection import get_db
from database.models import User
from config.env_setup import jwt_secret, jwt_algorithm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Extract user from JWT token and return the user object."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, jwt_secret, algorithms=[jwt_algorithm])
        username: str = payload.get("sub")
        user_id: int = payload.get("user_id")

        if username is None or user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    # Query the database for the user
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise credentials_exception

    return user
