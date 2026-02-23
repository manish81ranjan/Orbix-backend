# app/config.py
import os
from datetime import timedelta

class Config:
    MONGO_URI = os.getenv("MONGO_URI", "")
    JWT_SECRET = os.getenv("JWT_SECRET", "orbix-jwt-fallback")

    # ✅ comma-separated string in Render ENV (we will parse in extensions.py)
    CORS_ORIGINS = os.getenv(
        "CORS_ORIGINS",
        "https://orbix-frontend-1c18.vercel.app,http://localhost:5173"
    )

    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", str(20 * 1024 * 1024)))  # 20MB

    @staticmethod
    def jwt_expiry():
        return timedelta(days=7)
