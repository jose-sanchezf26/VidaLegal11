import os
from dotenv import load_dotenv
from itsdangerous import URLSafeTimedSerializer

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
ADMIN_USER = os.getenv("ADMIN_USER", "admin")
ADMIN_PASS = os.getenv("ADMIN_PASS", "admin1234")

serializer = URLSafeTimedSerializer(SECRET_KEY, salt="auth")

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL")

settings = Settings()