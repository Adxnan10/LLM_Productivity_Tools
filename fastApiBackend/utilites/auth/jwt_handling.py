import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException
from config.env_setup import jwt_secret, jwt_algorithm


ACCESS_TOKEN_EXPIRE_MINUTES = 43200  # Token expires in 30 days


def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    """Create a JWT token."""
    to_encode = data.copy()
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, jwt_secret, algorithm=jwt_algorithm)
    return encoded_jwt


def verify_access_token(token: str):
    """Verify the JWT token."""
    try:
        payload = jwt.decode(token, jwt_secret, algorithms=[jwt_algorithm])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
