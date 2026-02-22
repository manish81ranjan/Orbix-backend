# # from flask import Blueprint, request, jsonify
# # from app.services.auth_service import register_user, login_user

# # auth_bp = Blueprint("auth", __name__)


# # @auth_bp.route("/register", methods=["POST"])
# # def register():
# #     data = request.get_json(force=True) or {}
# #     try:
# #         res = register_user(
# #             data.get("username", ""),
# #             data.get("email", ""),
# #             data.get("password", "")
# #         )
# #         return jsonify(res), 201

# #     except ValueError as e:
# #         # Expected validation errors
# #         return jsonify({"message": str(e)}), 400

# #     except RuntimeError as e:
# #         # DB errors wrapped as RuntimeError
# #         return jsonify({"message": str(e)}), 500

# #     except Exception as e:
# #         # Any unknown crash
# #         return jsonify({"message": f"Internal server error: {e}"}), 500


# # @auth_bp.route("/login", methods=["POST"])
# # def login():
# #     data = request.get_json(force=True) or {}
# #     try:
# #         res = login_user(data.get("email", ""), data.get("password", ""))
# #         return jsonify(res), 200

# #     except ValueError as e:
# #         return jsonify({"message": str(e)}), 401

# #     except Exception as e:
# #         return jsonify({"message": f"Internal server error: {e}"}), 500
# from flask import Blueprint, request
# from app.services.auth_service import register_user, login_user

# auth_bp = Blueprint("auth", __name__)

# @auth_bp.post("/register")
# def register():
#     data = request.get_json(silent=True) or {}
#     return register_user(data)

# @auth_bp.post("/login")
# def login():
#     data = request.get_json(silent=True) or {}
#     return login_user(data)
# from flask import Blueprint, request, jsonify
# from app.services.auth_service import register_user, login_user

# auth_bp = Blueprint("auth", __name__)

# @auth_bp.route("/register", methods=["POST"])
# def register():
#     data = request.get_json(silent=True) or {}

#     username = data.get("username")
#     email = data.get("email")
#     password = data.get("password")

#     return register_user(username, email, password)


# @auth_bp.route("/login", methods=["POST"])
# def login():
#     data = request.get_json(silent=True) or {}

#     email = data.get("email")
#     password = data.get("password")

#     return login_user(email, password)
# from flask import Blueprint, request, jsonify, g
# from app.middleware.auth_required import auth_required
# from app.services.auth_service import register_user, login_user

# auth_bp = Blueprint("auth", __name__)

# @auth_bp.post("/register")
# def register():
#     data = request.get_json(silent=True) or {}
#     return register_user(data.get("username"), data.get("email"), data.get("password"))

# @auth_bp.post("/login")
# def login():
#     data = request.get_json(silent=True) or {}
#     return login_user(data.get("email"), data.get("password"))

# # ✅ ADD THIS
# @auth_bp.get("/me")
# @auth_required
# def me():
#     return jsonify({"user": g.current_user}), 200
# from flask import Blueprint, request, jsonify, g
# from app.middleware.auth_required import auth_required
# from app.services.auth_service import register_user, login_user

# auth_bp = Blueprint("auth", __name__)

# @auth_bp.post("/register")
# def register():
#     data = request.get_json(silent=True) or {}
#     return register_user(data.get("username"), data.get("email"), data.get("password"))

# @auth_bp.post("/login")
# def login():
#     data = request.get_json(silent=True) or {}
#     return login_user(data.get("email"), data.get("password"))

# # ✅ REQUIRED by frontend: GET /api/auth/me
# @auth_bp.get("/me")
# @auth_required
# def me():
#     return jsonify({"user": g.current_user}), 200
# from flask import Blueprint, request, jsonify, g
# from app.middleware.auth_required import auth_required
# from app.services.auth_service import register_user, login_user
# from app.models.user_model import get_user_by_id, serialize_user

# auth_bp = Blueprint("auth", __name__)

# @auth_bp.route("/register", methods=["POST", "OPTIONS"])
# def register():
#     if request.method == "OPTIONS":
#         return ("", 204)
#     data = request.get_json(silent=True) or {}
#     return register_user(data.get("username"), data.get("email"), data.get("password"))

# @auth_bp.route("/login", methods=["POST", "OPTIONS"])
# def login():
#     if request.method == "OPTIONS":
#         return ("", 204)
#     data = request.get_json(silent=True) or {}
#     return login_user(data.get("email"), data.get("password"))

# @auth_bp.route("/me", methods=["GET", "OPTIONS"])
# @auth_required
# def me():
#     # ✅ now works with token
#     user = get_user_by_id(g.user_id)
#     if not user:
#         return jsonify({"error": "User not found"}), 404
#     return jsonify({"user": serialize_user(user)}), 200
# from flask import Blueprint, request, jsonify, g
# import jwt
# from datetime import datetime
# from app.config import Config
# from app.extensions import hash_password, check_password
# from app.middleware.auth_required import auth_required
# from app.models.user_model import (
#     create_user, get_user_by_email, get_user_by_username, get_user_by_id, serialize_user
# )

# auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

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

# @auth_bp.route("/register", methods=["POST"])
# def register():
#     data = request.get_json(silent=True) or {}
#     username = (data.get("username") or "").strip()
#     email = (data.get("email") or "").strip().lower()
#     password = (data.get("password") or "")

#     if not username or not email or not password:
#         return jsonify({"error": "All fields are required"}), 400
#     if get_user_by_email(email):
#         return jsonify({"error": "Email already exists"}), 409
#     if get_user_by_username(username):
#         return jsonify({"error": "Username already taken"}), 409

#     user = create_user(username, email, hash_password(password))
#     return jsonify({"token": _issue_token(user), "user": serialize_user(user)}), 201

# @auth_bp.route("/login", methods=["POST"])
# def login():
#     data = request.get_json(silent=True) or {}
#     email = (data.get("email") or "").strip().lower()
#     password = (data.get("password") or "")

#     user = get_user_by_email(email)
#     if not user:
#         return jsonify({"error": "Invalid credentials"}), 401

#     hashed = user.get("password_hash") or user.get("password")
#     if not check_password(password, hashed):
#         return jsonify({"error": "Invalid credentials"}), 401

#     return jsonify({"token": _issue_token(user), "user": serialize_user(user)}), 200

# @auth_bp.route("/me", methods=["GET"])
# @auth_required
# def me():
#     user = get_user_by_id(g.user_id)
#     if not user:
#         return jsonify({"error": "User not found"}), 404
#     return jsonify({"user": serialize_user(user)}), 200

# app/routes/auth_routes.py
from flask import Blueprint, request, jsonify, g
import jwt
from datetime import datetime
from app.config import Config
from app.extensions import hash_password, check_password
from app.middleware.auth_required import auth_required
from app.models.user_model import (
    create_user, get_user_by_email, get_user_by_username, get_user_by_id, serialize_user
)

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

def _issue_token(user):
    payload = {
        "sub": str(user["_id"]),
        "email": user.get("email", ""),
        "username": user.get("username", ""),
        "iat": int(datetime.utcnow().timestamp()),
        "exp": int((datetime.utcnow() + Config.jwt_expiry()).timestamp()),
    }
    token = jwt.encode(payload, Config.JWT_SECRET, algorithm="HS256")
    return token if isinstance(token, str) else token.decode()

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = (data.get("password") or "")

    if not username or not email or not password:
        return jsonify({"error": "All fields are required"}), 400
    if get_user_by_email(email):
        return jsonify({"error": "Email already exists"}), 409
    if get_user_by_username(username):
        return jsonify({"error": "Username already taken"}), 409

    user = create_user(username, email, password)
    return jsonify({"token": _issue_token(user), "user": serialize_user(user)}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = (data.get("password") or "")

    user = get_user_by_email(email)
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    pw_hash = user.get("password_hash") or user.get("password") or ""
    if not check_password(password, pw_hash):
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify({"token": _issue_token(user), "user": serialize_user(user)}), 200

@auth_bp.route("/me", methods=["GET"])
@auth_required
def me():
    user = get_user_by_id(g.user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"user": serialize_user(user)}), 200