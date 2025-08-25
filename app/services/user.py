from app.schemas.user_schema import UserCreate, User as UserSchema
from app.db.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from app.utils.hashing import get_password_hash
from app.models import User

def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)

    db_user = User(
        email=user.email,
        fullname=user.fullname,
        password=hashed_password,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def get_user(email:str, db: Session = Depends(get_db)) -> UserSchema | None:
    return db.query(User).filter(User.email == email).first()
