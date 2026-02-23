# from flask import Flask
# from flask_cors import CORS
# from pymongo import MongoClient
# import bcrypt

# _mongo_client = None
# _mongo_db = None


# def init_extensions(app: Flask):
#     global _mongo_client, _mongo_db

#     _mongo_client = MongoClient(app.config["MONGO_URI"])
#     _mongo_db = _mongo_client.get_default_database()

#     CORS(
#         app,
#         resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}},
#         supports_credentials=True
#     )

#     return _mongo_db


# def get_db():
#     if _mongo_db is None:
#         raise RuntimeError("MongoDB not initialized. Did you call init_extensions(app)?")
#     return _mongo_db


# def hash_password(password: str) -> bytes:
#     return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


# def check_password(password: str, hashed: bytes) -> bool:
#     return bcrypt.checkpw(password.encode("utf-8"), hashed)
# from pymongo import MongoClient
# from flask_bcrypt import Bcrypt

# _client = None
# _db = None

# bcrypt = Bcrypt()

# def init_extensions(app):
#     """
#     Initializes MongoDB + Bcrypt.
#     """
#     global _client, _db

#     bcrypt.init_app(app)

#     mongo_uri = app.config.get("MONGO_URI")
#     _client = MongoClient(mongo_uri)
#     _db = _client.get_default_database()

#     return _db


# def get_db():
#     if _db is None:
#         raise RuntimeError("DB not initialized. Call init_extensions(app) first.")
#     return _db


# # ✅ BACKWARD-COMPAT: some files expect mongo_db
# def mongo_db():
#     """
#     Backward compatible alias for older code that imports mongo_db.
#     Usage: db = mongo_db()
#     """
#     return get_db()


# # ---------------- PASSWORD HELPERS ----------------
# def hash_password(password: str) -> bytes:
#     if not password:
#         raise ValueError("Password is required")
#     return bcrypt.generate_password_hash(password)


# def check_password(password: str, password_hash) -> bool:
#     if not password or not password_hash:
#         return False
#     return bcrypt.check_password_hash(password_hash, password)
# from flask import Flask
# from flask_cors import CORS
# from pymongo import MongoClient
# from flask_bcrypt import Bcrypt

# bcrypt = Bcrypt()

# _client = None
# _db = None


# def init_extensions(app: Flask):
#     """
#     Initialize MongoDB + Bcrypt + CORS
#     """
#     global _client, _db

#     # CORS
#     origins = app.config.get("CORS_ORIGINS", "*")
#     CORS(app, resources={r"/api/*": {"origins": origins}})


#     # Bcrypt
#     bcrypt.init_app(app)

#     # Mongo
#     mongo_uri = app.config.get("MONGO_URI")
#     if not mongo_uri:
#         raise RuntimeError("MONGO_URI is not set")

#     _client = MongoClient(mongo_uri)
#     _db = _client.get_default_database()  # gets "orbix" from URI


# def get_db():
#     if _db is None:
#         raise RuntimeError("MongoDB not initialized. Did you call init_extensions(app)?")
#     return _db


# # ✅ These are REQUIRED by auth_service.py
# def hash_password(password: str) -> str:
#     return bcrypt.generate_password_hash(password).decode("utf-8")


# def check_password(password: str, password_hash: str) -> bool:
#     return bcrypt.check_password_hash(password_hash, password)
# from flask import Flask
# from flask_bcrypt import Bcrypt
# from flask_pymongo import PyMongo

# mongo = PyMongo()
# bcrypt = Bcrypt()

# _db = None  # cached database object


# def init_extensions(app: Flask):
#     """
#     Initialize Mongo + Bcrypt
#     """
#     global _db
#     mongo.init_app(app)
#     bcrypt.init_app(app)
#     _db = mongo.db


# def get_db():
#     """
#     Returns MongoDB database object safely
#     """
#     global _db
#     if _db is None:
#         # fallback if init_extensions ran but cache not set
#         if mongo.db is not None:
#             _db = mongo.db
#         else:
#             raise RuntimeError("MongoDB not initialized. Did you call init_extensions(app)?")
#     return _db


# # ✅ PASSWORD HELPERS (FIXED)
# def hash_password(password: str) -> str:
#     """
#     Always return a STRING hash (utf-8)
#     """
#     return bcrypt.generate_password_hash(password).decode("utf-8")


# def check_password(password: str, hashed) -> bool:
#     """
#     Works with both:
#     - hashed as bytes (old saved users)
#     - hashed as str  (new saved users)
#     """
#     if hashed is None:
#         return False

#     # if bytes -> decode to str
#     if isinstance(hashed, (bytes, bytearray)):
#         hashed = hashed.decode("utf-8", errors="ignore")

#     return bcrypt.check_password_hash(hashed, password)
# from flask import Flask
# from flask_cors import CORS
# from flask_pymongo import PyMongo
# from werkzeug.security import generate_password_hash, check_password_hash

# mongo = PyMongo()

# def init_extensions(app: Flask):
#     origins = app.config.get("CORS_ORIGINS", ["http://localhost:5173"])

#     # ✅ CORS for /api/*
#     CORS(
#         app,
#         resources={r"/api/*": {"origins": origins}},
#         supports_credentials=False,
#         allow_headers=["Content-Type", "Authorization"],
#         methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
#         max_age=86400,
#     )

#     mongo.init_app(app)

# def get_db():
#     db = mongo.db
#     if db is None:
#         raise RuntimeError("MongoDB not initialized. Did you call init_extensions(app)?")
#     return db

# # ✅ these names are used by auth_service
# def hash_password(password: str) -> str:
#     return generate_password_hash(password)

# def check_password(password: str, hashed: str) -> bool:
#     return check_password_hash(hashed, password)
# app/extensions.py

# from flask import Flask
# from flask_cors import CORS
# from flask_pymongo import PyMongo
# from werkzeug.security import generate_password_hash, check_password_hash

# mongo = PyMongo()

# def init_extensions(app: Flask):
#     origins = app.config.get("CORS_ORIGINS", "http://localhost:5173")
#     if isinstance(origins, str):
#         origins = [o.strip() for o in origins.split(",") if o.strip()]

#     CORS(
#         app,
#         resources={r"/api/*": {"origins": origins}},
#         supports_credentials=False,
#         allow_headers=["Content-Type", "Authorization"],
#         methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
#         max_age=86400,
#     )

#     mongo.init_app(app)

# def get_db():
#     db = mongo.db
#     if db is None:
#         raise RuntimeError("MongoDB not initialized. Did you call init_extensions(app)?")
#     return db

# def hash_password(password: str) -> str:
#     if password is None:
#         password = ""
#     if not isinstance(password, str):
#         password = str(password)
#     return generate_password_hash(password)

# def check_password(password: str, hashed) -> bool:
#     if not hashed:
#         return False
#     if isinstance(hashed, (bytes, bytearray)):
#         hashed = bytes(hashed).decode("utf-8", errors="ignore")
#     if password is None:
#         password = ""
#     if not isinstance(password, str):
#         password = str(password)
#     try:
#         return check_password_hash(hashed, password)
#     except Exception:
#         return False

# import os
# from pymongo import MongoClient
# from flask_cors import CORS

# _client = None
# _db = None


# def init_extensions(app):
#     """
#     - MongoDB connection
#     - CORS (supports Authorization header + multipart)
#     """

#     global _client, _db

#     mongo_uri = os.environ.get("MONGO_URI") or os.environ.get("DATABASE_URL") or getattr(
#         app.config, "MONGO_URI", None
#     ) or app.config.get("MONGO_URI")

#     if not mongo_uri:
#         raise RuntimeError("Missing MONGO_URI in environment/config")

#     db_name = os.environ.get("MONGO_DB") or app.config.get("MONGO_DB") or "orbix"

#     _client = MongoClient(mongo_uri)
#     _db = _client[db_name]

#     # ✅ CORS
#     origins = os.environ.get("CORS_ORIGINS") or app.config.get("CORS_ORIGINS") or "http://localhost:5173"
#     if isinstance(origins, str):
#         origins = [o.strip() for o in origins.split(",") if o.strip()]

#     CORS(
#         app,
#         resources={r"/api/*": {"origins": origins}},
#         supports_credentials=False,
#         allow_headers=["Content-Type", "Authorization"],
#         methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
#         max_age=86400,
#     )

#     # Add headers on every response (including errors)
#     @app.after_request
#     def add_headers(resp):
#         resp.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
#         resp.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
#         return resp


# def get_db():
#     if _db is None:
#         raise RuntimeError("MongoDB not initialized. Did you call init_extensions(app)?")
#     return _db

# from __future__ import annotations

# from flask import Flask
# from flask_cors import CORS
# from flask_pymongo import PyMongo
# from werkzeug.security import generate_password_hash, check_password_hash

# mongo = PyMongo()


# def init_extensions(app: Flask):
#     """
#     - Initializes Mongo
#     - Enables CORS for /api/*
#     """
#     origins = app.config.get("CORS_ORIGINS", ["http://localhost:5173"])

#     CORS(
#         app,
#         resources={r"/api/*": {"origins": origins}},
#         supports_credentials=False,
#         allow_headers=["Content-Type", "Authorization"],
#         methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
#         max_age=86400,
#     )

#     mongo.init_app(app)


# def get_db():
#     db = mongo.db
#     if db is None:
#         raise RuntimeError("MongoDB not initialized. Did you call init_extensions(app)?")
#     return db


# # -------------------- PASSWORD HELPERS (FIX) --------------------
# def hash_password(password: str) -> str:
#     """
#     Always returns a STRING hash (Werkzeug expects str).
#     """
#     return generate_password_hash(password)


# def check_password(password: str, hashed) -> bool:
#     """
#     Supports both str and bytes stored hash.
#     Fixes: 'a bytes-like object is required, not str'
#     """
#     if hashed is None:
#         return False

#     # Mongo may contain bytes from old inserts
#     if isinstance(hashed, (bytes, bytearray)):
#         try:
#             hashed = hashed.decode("utf-8")
#         except Exception:
#             return False

#     # Werkzeug signature: check_password_hash(pwhash, password)
#     return check_password_hash(str(hashed), password)

# # app/extensions.py
# from flask_pymongo import PyMongo
# from flask_bcrypt import Bcrypt
# from flask_jwt_extended import JWTManager
# from flask_cors import CORS

# mongo = PyMongo()
# bcrypt = Bcrypt()
# jwt = JWTManager()


# def init_extensions(app):
#     """
#     Initializes:
#     - MongoDB
#     - Bcrypt
#     - JWT
#     - CORS (API-safe)
#     """
#     # ---- CORS ----
#     origins = app.config.get("CORS_ORIGINS") or ["http://localhost:5173"]
#     if origins == "*" or origins == ["*"]:
#         origins = "*"

#     CORS(
#         app,
#         resources={r"/api/*": {"origins": origins}},
#         supports_credentials=False,
#         allow_headers=["Content-Type", "Authorization"],
#         methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
#     )

#     mongo.init_app(app)
#     bcrypt.init_app(app)
#     jwt.init_app(app)


# def get_db():
#     return mongo.db


# def hash_password(password: str) -> str:
#     return bcrypt.generate_password_hash(password).decode("utf-8")


# def check_password(password: str, hashed: str) -> bool:
#     try:
#         return bcrypt.check_password_hash(hashed, password)
#     except Exception:

#         return False


# # app/extensions.py
# from flask_pymongo import PyMongo
# from flask_bcrypt import Bcrypt
# from flask_jwt_extended import JWTManager
# from flask_cors import CORS

# mongo = PyMongo()
# bcrypt = Bcrypt()
# jwt = JWTManager()


# def _parse_origins(value):
#     """
#     Accepts:
#     - None
#     - "*" (not recommended)
#     - "a,b,c"
#     - ["a", "b"]
#     Returns: list[str] or "*"
#     """
#     if not value:
#         return ["http://localhost:5173"]

#     if isinstance(value, (list, tuple)):
#         origins = [str(x).strip().rstrip("/") for x in value if str(x).strip()]
#         return origins or ["http://localhost:5173"]

#     value = str(value).strip()

#     if value == "*":
#         return "*"  # not recommended for auth APIs

#     origins = [o.strip().rstrip("/") for o in value.split(",") if o.strip()]
#     return origins or ["http://localhost:5173"]


# def init_extensions(app):
#     # ---- CORS ----
#     origins = _parse_origins(app.config.get("CORS_ORIGINS"))

#     CORS(
#         app,
#         resources={r"/api/*": {"origins": origins}},
#         supports_credentials=False,
#         allow_headers=["Content-Type", "Authorization"],
#         methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
#     )

#     mongo.init_app(app)
#     bcrypt.init_app(app)
#     jwt.init_app(app)


# def get_db():
#     return mongo.db


# def hash_password(password: str) -> str:
#     return bcrypt.generate_password_hash(password).decode("utf-8")


# def check_password(password: str, hashed: str) -> bool:
#     try:
#         return bcrypt.check_password_hash(hashed, password)
#     except Exception:
#         return False


# app/extensions.py
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS

mongo = PyMongo()
bcrypt = Bcrypt()
jwt = JWTManager()


def _parse_origins(value):
    """
    Accepts:
    - None
    - "*" (not recommended)
    - "a,b,c"
    - ["a", "b"]
    Returns: list[str] or "*"
    """
    if not value:
        return ["http://localhost:5173"]

    if isinstance(value, (list, tuple)):
        origins = [str(x).strip().rstrip("/") for x in value if str(x).strip()]
        return origins or ["http://localhost:5173"]

    value = str(value).strip()

    if value == "*":
        return "*"  # not recommended for auth APIs

    origins = [o.strip().rstrip("/") for o in value.split(",") if o.strip()]
    return origins or ["http://localhost:5173"]


def init_extensions(app):
    """
    Initializes:
    - MongoDB
    - Bcrypt
    - JWT
    - CORS (API-safe)
    """
    origins = _parse_origins(app.config.get("CORS_ORIGINS"))

    CORS(
        app,
        resources={r"/api/*": {"origins": origins}},
        supports_credentials=False,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    )

    mongo.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)


def get_db():
    return mongo.db


def hash_password(password: str) -> str:
    return bcrypt.generate_password_hash(password).decode("utf-8")


def check_password(password: str, hashed: str) -> bool:
    try:
        return bcrypt.check_password_hash(hashed, password)
    except Exception:
        return False

