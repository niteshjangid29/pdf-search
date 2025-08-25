from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.utils.token import verify_access_token
from app.services.user import get_user
from app.db.database import get_db
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verify_access_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = get_user(payload.get("email"), db)

    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user
