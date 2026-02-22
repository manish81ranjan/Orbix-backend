# # # import os
# # # from datetime import timedelta
# # # from dotenv import load_dotenv

# # # # Load .env if present
# # # load_dotenv()


# # # class Config:
# # #     """Base configuration for Orbix backend"""

# # #     # Flask
# # #     SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret")
# # #     ENV = os.getenv("FLASK_ENV", "production")

# # #     # Server
# # #     PORT = int(os.getenv("PORT", 5000))

# # #     # MongoDB
# # #     MONGO_URI = os.getenv("MONGO_URI")

# # #     if not MONGO_URI:
# # #         raise RuntimeError("MONGO_URI is not set. Please configure MongoDB Atlas.")

# # #     # JWT
# # #     JWT_SECRET = os.getenv("JWT_SECRET", "change-this-jwt-secret")
# # #     JWT_EXPIRES_IN = os.getenv("JWT_EXPIRES_IN", "7d")

# # #     # Convert JWT_EXPIRES_IN to timedelta
# # #     @staticmethod
# # #     def jwt_expiry():
# # #         val = Config.JWT_EXPIRES_IN.lower()
# # #         if val.endswith("d"):
# # #             return timedelta(days=int(val[:-1]))
# # #         if val.endswith("h"):
# # #             return timedelta(hours=int(val[:-1]))
# # #         return timedelta(days=7)

# # #     # CORS
# # #     CORS_ORIGINS = [
# # #         origin.strip()
# # #         for origin in os.getenv("CORS_ORIGINS", "*").split(",")
# # #     ]

# # import os
# # from dotenv import load_dotenv

# # load_dotenv()

# # class Config:
# #     SECRET_KEY = os.getenv("SECRET_KEY", "orbix-secret")
# #     MONGO_URI = os.getenv("MONGO_URI", "mongodb://127.0.0.1:27017/orbix")

# #     # If you're using JWT later
# #     JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", SECRET_KEY)

# #     # CORS if you need later
# #     CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
# import os
# from datetime import timedelta
# from dotenv import load_dotenv

# load_dotenv()


# class Config:
#     # -----------------------------
#     # Flask / App
#     # -----------------------------
#     ENV = os.getenv("FLASK_ENV", "development")
#     SECRET_KEY = os.getenv("SECRET_KEY", "orbix-secret")

#     # -----------------------------
#     # Server
#     # -----------------------------
#     PORT = int(os.getenv("PORT", 5000))

#     # -----------------------------
#     # MongoDB
#     # -----------------------------
#     MONGO_URI = os.getenv("MONGO_URI", "mongodb://127.0.0.1:27017/orbix")

#     # -----------------------------
#     # JWT (supports BOTH names)
#     # -----------------------------
#     # Your .env uses JWT_SECRET
#     # Some code may use JWT_SECRET_KEY
#     JWT_SECRET = os.getenv("JWT_SECRET") or os.getenv("JWT_SECRET_KEY") or SECRET_KEY
#     JWT_SECRET_KEY = JWT_SECRET  # alias to keep old code working

#     JWT_EXPIRES_IN = os.getenv("JWT_EXPIRES_IN", "7d")

#     @staticmethod
#     def jwt_expiry() -> timedelta:
#         val = (Config.JWT_EXPIRES_IN or "7d").strip().lower()
#         try:
#             if val.endswith("d"):
#                 return timedelta(days=int(val[:-1]))
#             if val.endswith("h"):
#                 return timedelta(hours=int(val[:-1]))
#             if val.endswith("m"):
#                 return timedelta(minutes=int(val[:-1]))
#             if val.endswith("s"):
#                 return timedelta(seconds=int(val[:-1]))
#         except Exception:
#             pass
#         return timedelta(days=7)

#     # -----------------------------
#     # CORS
#     # -----------------------------
#     CORS_ORIGINS = [o.strip() for o in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")]
# import os
# from datetime import timedelta
# from dotenv import load_dotenv

# load_dotenv()

# class Config:
#     # Flask
#     SECRET_KEY = os.getenv("SECRET_KEY", "orbix-secret")

#     # MongoDB
#     MONGO_URI = os.getenv("MONGO_URI", "mongodb://127.0.0.1:27017/orbix")

#     # ✅ JWT – SAFE, NO KeyError POSSIBLE
#     JWT_SECRET = os.getenv("JWT_SECRET") or os.getenv("JWT_SECRET_KEY") or SECRET_KEY
#     JWT_SECRET_KEY = JWT_SECRET   # alias for older code

#     JWT_EXPIRES_IN = os.getenv("JWT_EXPIRES_IN", "7d")

#     @staticmethod
#     def jwt_expiry():
#         val = (Config.JWT_EXPIRES_IN or "7d").lower()
#         if val.endswith("d"):
#             return timedelta(days=int(val[:-1]))
#         if val.endswith("h"):
#             return timedelta(hours=int(val[:-1]))
#         return timedelta(days=7)
# import os
# from datetime import timedelta
# from dotenv import load_dotenv

# load_dotenv()

# class Config:
#     SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret")
#     ENV = os.getenv("FLASK_ENV", "production")
#     PORT = int(os.getenv("PORT", 5000))

#     MONGO_URI = os.getenv("MONGO_URI")

#     JWT_SECRET = os.getenv("JWT_SECRET", "change-this-jwt-secret")
#     JWT_EXPIRES_IN = os.getenv("JWT_EXPIRES_IN", "7d")

#     CORS_ORIGINS = [o.strip() for o in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")]

#     @staticmethod
#     def jwt_expiry():
#         val = (Config.JWT_EXPIRES_IN or "7d").lower().strip()
#         if val.endswith("d"):
#             return timedelta(days=int(val[:-1]))
#         if val.endswith("h"):
#             return timedelta(hours=int(val[:-1]))
#         return timedelta(days=7)
# import os
# from datetime import timedelta
# from dotenv import load_dotenv

# load_dotenv()

# class Config:
#     SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret")
#     ENV = os.getenv("FLASK_ENV", "development")
#     PORT = int(os.getenv("PORT", 5000))

#     MONGO_URI = os.getenv("MONGO_URI")
#     JWT_SECRET = os.getenv("JWT_SECRET", "change-this-jwt-secret")
#     JWT_EXPIRES_IN = os.getenv("JWT_EXPIRES_IN", "7d")

#     @staticmethod
#     def jwt_expiry():
#         val = (Config.JWT_EXPIRES_IN or "7d").lower()
#         if val.endswith("d"):
#             return timedelta(days=int(val[:-1]))
#         if val.endswith("h"):
#             return timedelta(hours=int(val[:-1]))
#         return timedelta(days=7)

#     # ✅ Must be list
#     CORS_ORIGINS = [o.strip() for o in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")]
import os
from datetime import timedelta

class Config:
    MONGO_URI = os.getenv("MONGO_URI", "")
    JWT_SECRET = os.getenv("JWT_SECRET", "orbix-jwt-fallback")
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "https://orbix-frontend-1c18.vercel.app/")
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", str(20 * 1024 * 1024)))  # 20MB

    @staticmethod
    def jwt_expiry():

        return timedelta(days=7)
