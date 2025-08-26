import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "")
    EXPIRY_TIME: int = int(os.getenv("EXPIRY_TIME", 60))
    ES_HOST: str = os.getenv("ES_HOST", "")
    ES_API_KEY: str = os.getenv("ES_API_KEY", "")
    INDEX_NAME: str = os.getenv("INDEX_NAME", "")

settings = Settings()
