import os
from dotenv import load_dotenv

load_dotenv()  # load variables from .env

class Settings:
    PROJECT_NAME: str = "Linkedin Profile Manager"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    API_KEY: str = os.getenv("API_KEY", "")

settings = Settings()
