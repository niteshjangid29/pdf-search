import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "")
    EXPIRY_TIME: int = int(os.getenv("EXPIRY_TIME", 60))

settings = Settings()
