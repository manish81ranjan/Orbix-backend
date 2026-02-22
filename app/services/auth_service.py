# """
# Auth service
# - Handles register / login / current user logic
# """

# from pymongo.errors import DuplicateKeyError

# from app.models.user_model import (
#     create_user,
#     get_user_by_email,
#     get_user_by_username,
#     get_user_by_id,
#     serialize_user
# )
# from app.extensions import hash_password, check_password
# from app.utils.security import create_jwt
# from app.utils.validators import is_email, min_length


# def register_user(username: str, email: str, password: str):
#     username = (username or "").strip()
#     email = (email or "").strip().lower()

#     if not min_length(username, 3):
#         raise ValueError("Username must be at least 3 characters")

#     if not is_email(email):
#         raise ValueError("Invalid email address")

#     if not min_length(password, 6):
#         raise ValueError("Password must be at least 6 characters")

#     # pre-checks (nice UX)
#     if get_user_by_email(email):
#         raise ValueError("Email already registered")

#     if get_user_by_username(username):
#         raise ValueError("Username already taken")

#     password_hash = hash_password(password)

#     try:
#         user = create_user(username, email, password_hash)
#     except DuplicateKeyError:
#         # If index triggers (race / double click)
#         raise ValueError("Email or username already exists")
#     except Exception as e:
#         # Any other DB issue
#         raise RuntimeError(f"Register failed: {e}")

#     token = create_jwt(str(user["_id"]))
#     return {
#         "token": token,
#         "user": serialize_user(user)
#     }


# def login_user(email: str, password: str):
#     email = (email or "").strip().lower()
#     password = password or ""

#     if not email or not password:
#         raise ValueError("Email and password required")

#     user = get_user_by_email(email)
#     if not user:
#         raise ValueError("Invalid credentials")

#     if not check_password(password, user["password"]):
#         raise ValueError("Invalid credentials")

#     token = create_jwt(str(user["_id"]))
#     return {
#         "token": token,
#         "user": serialize_user(user)
#     }


# def get_current_user(user_id: str):
#     user = get_user_by_id(user_id)
#     if not user:
#         raise ValueError("User not found")
#     return serialize_user(user)
# from flask import jsonify
# import jwt
# from datetime import datetime
# from app.extensions import hash_password, check_password, get_db

# from app.config import Config
# # from app.extensions import hash_password, check_password
# from app.models.user_model import (
#     create_user,
#     get_user_by_email,
#     get_user_by_username,
#     serialize_user,
# )

# def _issue_token(user):
#     payload = {
#         "sub": str(user["_id"]),
#         "email": user["email"],
#         "username": user["username"],
#         "iat": int(datetime.utcnow().timestamp()),
#         "exp": int((datetime.utcnow() + Config.jwt_expiry()).timestamp()),
#     }
#     token = jwt.encode(payload, Config.JWT_SECRET, algorithm="HS256")
#     return token if isinstance(token, str) else token.decode()


# def register_user(username, email, password):
#     if not username or not email or not password:
#         return jsonify({"error": "All fields are required"}), 400

#     if get_user_by_email(email):
#         return jsonify({"error": "Email already exists"}), 409

#     if get_user_by_username(username):
#         return jsonify({"error": "Username already taken"}), 409

#     user = create_user(
#         username=username.strip(),
#         email=email.strip().lower(),
#         password_hash=hash_password(password),
#     )

#     token = _issue_token(user)

#     return jsonify({
#         "message": "Registered successfully",
#         "token": token,
#         "user": serialize_user(user),
#     }), 201


# def login_user(email, password):
#     if not email or not password:
#         return jsonify({"error": "Email and password required"}), 400

#     user = get_user_by_email(email.strip().lower())
#     if not user or not check_password(password, user["password"]):
#         return jsonify({"error": "Invalid credentials"}), 401

#     token = _issue_token(user)

#     return jsonify({
#         "message": "Login successful",
#         "token": token,
#         "user": serialize_user(user),
#     }), 200
from flask import jsonify
import jwt
from datetime import datetime
from app.extensions import hash_password, check_password
from app.config import Config
from app.models.user_model import (
    create_user,
    get_user_by_email,
    get_user_by_username,
    serialize_user,
)

def _issue_token(user):
    payload = {
        "sub": str(user["_id"]),
        "email": user["email"],
        "username": user["username"],
        "iat": int(datetime.utcnow().timestamp()),
        "exp": int((datetime.utcnow() + Config.jwt_expiry()).timestamp()),
    }
    token = jwt.encode(payload, Config.JWT_SECRET, algorithm="HS256")
    return token if isinstance(token, str) else token.decode()


def register_user(username, email, password):
    if not username or not email or not password:
        return jsonify({"error": "All fields are required"}), 400

    if get_user_by_email(email):
        return jsonify({"error": "Email already exists"}), 409

    if get_user_by_username(username):
        return jsonify({"error": "Username already taken"}), 409

    user = create_user(
        username=username.strip(),
        email=email.strip().lower(),
        password_hash=hash_password(password),  # ✅ now always string
    )

    token = _issue_token(user)

    return jsonify({
        "message": "Registered successfully",
        "token": token,
        "user": serialize_user(user),
    }), 201


def login_user(email, password):
    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    user = get_user_by_email(email.strip().lower())
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    # ✅ support both keys
    
    hashed = user.get("password_hash") or user.get("password")
    if not hashed:
        return jsonify({"error": "Invalid credentials"}), 401
    if not check_password(password, hashed):
        return jsonify({"error": "Invalid credentials"}), 401

    token = _issue_token(user)

    return jsonify({
        "message": "Login successful",
        "token": token,
        "user": serialize_user(user),
    }), 200
