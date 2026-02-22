# """
# auth_required middleware
# - Verifies JWT
# - Attaches current_user to request context
# """

# from functools import wraps
# from flask import request, jsonify, current_app, g
# import jwt
# from datetime import datetime

# from app.extensions import mongo_db


# def auth_required(fn):
#     @wraps(fn)
#     def wrapper(*args, **kwargs):
#         auth_header = request.headers.get("Authorization", "")
#         if not auth_header.startswith("Bearer "):
#             return jsonify({"message": "Authorization token missing"}), 401

#         token = auth_header.split(" ", 1)[1]

#         try:
#             payload = jwt.decode(
#                 token,
#                 current_app.config["JWT_SECRET"],
#                 algorithms=["HS256"]
#             )

#             # Expiry check (extra safety)
#             if "exp" in payload and datetime.utcfromtimestamp(payload["exp"]) < datetime.utcnow():
#                 return jsonify({"message": "Token expired"}), 401

#             user_id = payload.get("sub")
#             if not user_id:
#                 return jsonify({"message": "Invalid token"}), 401

#             user = mongo_db.users.find_one(
#                 {"_id": user_id},
#                 {"password": 0}
#             )
#             if not user:
#                 return jsonify({"message": "User not found"}), 401

#             # Attach to request context
#             g.current_user = user

#         except jwt.ExpiredSignatureError:
#             return jsonify({"message": "Token expired"}), 401
#         except jwt.InvalidTokenError:
#             return jsonify({"message": "Invalid token"}), 401
#         except Exception:
#             return jsonify({"message": "Authentication failed"}), 401

#         return fn(*args, **kwargs)

#     return wrapper
# from functools import wraps
# from flask import request, jsonify, g
# import jwt
# from bson import ObjectId

# from app.config import Config
# from app.extensions import get_db


# def auth_required(fn):
#     @wraps(fn)
#     def wrapper(*args, **kwargs):
#         auth = request.headers.get("Authorization", "")
#         parts = auth.split()

#         if len(parts) != 2 or parts[0].lower() != "bearer":
#             return jsonify({"message": "Authorization token missing"}), 401

#         token = parts[1]

#         try:
#             payload = jwt.decode(token, Config.JWT_SECRET, algorithms=["HS256"])
#         except jwt.ExpiredSignatureError:
#             return jsonify({"message": "Token expired"}), 401
#         except jwt.InvalidTokenError:
#             return jsonify({"message": "Invalid token"}), 401

#         user_id = payload.get("sub")
#         if not user_id:
#             return jsonify({"message": "Invalid token"}), 401

#         try:
#             oid = ObjectId(user_id)
#         except Exception:
#             return jsonify({"message": "Invalid user id"}), 401

#         db = get_db()
#         user = db.users.find_one({"_id": oid}, {"password": 0})
#         if not user:
#             return jsonify({"message": "User not found"}), 401

#         user["_id"] = str(user["_id"])
#         g.current_user = user

#         return fn(*args, **kwargs)

#     return wrapper
# from functools import wraps
# from flask import request, jsonify, g
# from app.utils.security import decode_jwt

# def auth_required(fn):
#     @wraps(fn)
#     def wrapper(*args, **kwargs):
#         # ✅ Let preflight pass
#         if request.method == "OPTIONS":
#             return ("", 204)

#         auth = request.headers.get("Authorization", "")
#         if not auth.startswith("Bearer "):
#             return jsonify({"message": "Missing token"}), 401

#         token = auth.replace("Bearer ", "").strip()
#         try:
#             payload = decode_jwt(token)
#             g.user_id = payload.get("sub")
#             g.username = payload.get("username")
#             if not g.user_id:
#                 return jsonify({"message": "Invalid token"}), 401
#         except Exception:
#             return jsonify({"message": "Invalid or expired token"}), 401

#         return fn(*args, **kwargs)
#     return wrapper
# from functools import wraps
# from flask import request, jsonify, g
# import jwt
# from app.config import Config

# def auth_required(fn):
#     @wraps(fn)
#     def wrapper(*args, **kwargs):
#         # ✅ Let OPTIONS preflight pass
#         if request.method == "OPTIONS":
#             return ("", 204)

#         auth = request.headers.get("Authorization", "")
#         if not auth.startswith("Bearer "):
#             return jsonify({"error": "Missing Authorization Bearer token"}), 401

#         token = auth.replace("Bearer ", "").strip()
#         try:
#             payload = jwt.decode(token, Config.JWT_SECRET, algorithms=["HS256"])
#             g.user_id = payload.get("sub")
#             g.username = payload.get("username")
#         except Exception:
#             return jsonify({"error": "Invalid or expired token"}), 401

#         return fn(*args, **kwargs)
#     return wrapper
# from functools import wraps
# from flask import request, jsonify, g
# import jwt
# from app.config import Config

# def auth_required(fn):
#     @wraps(fn)
#     def wrapper(*args, **kwargs):
#         # ✅ handle OPTIONS without auth (preflight)
#         if request.method == "OPTIONS":
#             return ("", 204)

#         auth = request.headers.get("Authorization", "") or ""
#         token = ""

#         # Accept: Authorization: Bearer <token>
#         if auth.lower().startswith("bearer "):
#             token = auth.split(" ", 1)[1].strip()

#         # fallback header if you ever used it
#         if not token:
#             token = request.headers.get("x-access-token", "").strip()

#         if not token:
#             return jsonify({"error": "Missing token"}), 401

#         try:
#             payload = jwt.decode(token, Config.JWT_SECRET, algorithms=["HS256"])
#             g.user_id = payload.get("sub")
#             g.email = payload.get("email")
#             g.username = payload.get("username")
#         except jwt.ExpiredSignatureError:
#             return jsonify({"error": "Token expired"}), 401
#         except Exception:
#             return jsonify({"error": "Invalid token"}), 401

#         return fn(*args, **kwargs)
#     return wrapper


# from functools import wraps
# from flask import request, jsonify, g
# import jwt
# from app.config import Config

# def auth_required(fn):
#     @wraps(fn)
#     def wrapper(*args, **kwargs):
#         # ✅ Allow preflight
#         if request.method == "OPTIONS":
#             return ("", 204)

#         auth = request.headers.get("Authorization", "") or ""
#         token = ""

#         if auth.lower().startswith("bearer "):
#             token = auth.split(" ", 1)[1].strip()

#         if not token:
#             token = request.headers.get("x-access-token", "").strip()

#         if not token:
#             return jsonify({"error": "Missing token"}), 401

#         try:
#             payload = jwt.decode(token, Config.JWT_SECRET, algorithms=["HS256"])
#             g.user_id = payload.get("sub")
#             g.email = payload.get("email")
#             g.username = payload.get("username")

#             # ✅ convenient object for services/routes
#             g.current_user = {"_id": g.user_id, "email": g.email, "username": g.username}

#             if not g.user_id:
#                 return jsonify({"error": "Invalid token payload"}), 401

#         except jwt.ExpiredSignatureError:
#             return jsonify({"error": "Token expired"}), 401
#         except Exception:
#             return jsonify({"error": "Invalid token"}), 401

#         return fn(*args, **kwargs)

#     return wrapper

from functools import wraps
from flask import request, jsonify, g
import jwt
from app.config import Config


def auth_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # ✅ allow preflight without auth
        if request.method == "OPTIONS":
            return ("", 204)

        auth = request.headers.get("Authorization", "") or ""
        token = ""

        if auth.lower().startswith("bearer "):
            token = auth.split(" ", 1)[1].strip()

        if not token:
            token = request.headers.get("x-access-token", "").strip()

        if not token:
            return jsonify({"error": "Missing token"}), 401

        try:
            payload = jwt.decode(token, Config.JWT_SECRET, algorithms=["HS256"])
            g.user_id = payload.get("sub")
            g.email = payload.get("email")
            g.username = payload.get("username")

            # ✅ compatibility for other routes expecting g.current_user
            g.current_user = {
                "_id": g.user_id,
                "email": g.email,
                "username": g.username,
            }
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except Exception:
            return jsonify({"error": "Invalid token"}), 401

        return fn(*args, **kwargs)

    return wrapper