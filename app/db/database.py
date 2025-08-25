from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config.config import settings

from typing import Optional

engine = None
SessionLocal: Optional[sessionmaker] = None

Base = declarative_base()

def init_db():
    global engine, SessionLocal

    if engine is None:
        engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

    if SessionLocal is None:
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    print("Database initialized successfully.")

def create_all_tables():
    if engine is not None:
        Base.metadata.create_all(bind=engine)
    
    print("All tables created or already exist.")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
