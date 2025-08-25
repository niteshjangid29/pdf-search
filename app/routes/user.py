from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user_schema import User, UserCreate, UserLogin
from app.schemas.token_schema import Token, TokenData
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.services.user import create_user, get_user
from app.utils.hashing import verify_password
from app.utils.auth import get_current_user
from app.utils.token import create_access_token

router = APIRouter()

@router.post("/register", response_model=User)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user(user.email, db)

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    return create_user(user, db)

@router.post("/login", response_model=Token)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    existing_user = get_user(user.email, db)
    is_valid_password = verify_password(user.password, existing_user.password)

    if not existing_user or not is_valid_password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token_data = TokenData(id=str(existing_user.id), email=existing_user.email, password=existing_user.password)
    access_token = create_access_token(data=token_data.dict())

    return Token(access_token=access_token, token_type="bearer")

@router.get("/profile", response_model=User)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user
