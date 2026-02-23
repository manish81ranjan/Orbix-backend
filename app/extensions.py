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
    - "*" or ["*"] -> "*"
    - "https://a.com,http://localhost:5173" -> ["https://a.com", "http://localhost:5173"]
    - ["https://a.com", "http://localhost:5173"] -> same
    Removes trailing slashes to avoid mismatch.
    """
    if not value:
        return ["http://localhost:5173"]

    # If already list/tuple
    if isinstance(value, (list, tuple)):
        origins = [str(x).strip() for x in value if str(x).strip()]
    else:
        s = str(value).strip()
        if s == "*" or s.lower() == "all":
            return "*"
        # comma-separated
        origins = [x.strip() for x in s.split(",") if x.strip()]

    # normalize: remove trailing /
    origins = [o[:-1] if o.endswith("/") else o for o in origins]

    if origins == ["*"]:
        return "*"

    return origins


def init_extensions(app):
    """
    Initializes:
    - MongoDB
    - Bcrypt
    - JWT
    - CORS (API-safe)
    """
    origins = _parse_origins(app.config.get("CORS_ORIGINS"))

    # ✅ allow CORS for /api/* (and OPTIONS preflight)
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
