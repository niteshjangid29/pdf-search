from typing import Optional
from datetime import datetime, timedelta
from app.config.config import settings
from jose import jwt, JWTError

def create_access_token(data: dict, expires_delta: Optional[timedelta]=None) -> str:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.EXPIRY_TIME)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm="HS256")
    return encoded_jwt

def verify_access_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        expire_time = datetime.fromtimestamp(payload.get("exp"))
        is_valid = payload if expire_time >= datetime.utcnow() else None
        return is_valid
    except JWTError:
        return None
