# from datetime import datetime
# from bson import ObjectId
# from app.extensions import get_db


# def _oid(value: str):
#     try:
#         return ObjectId(value)
#     except Exception:
#         return None


# def serialize_user(user: dict) -> dict:
#     created = user.get("created_at")
#     return {
#         "_id": str(user.get("_id")),
#         "username": user.get("username"),
#         "email": user.get("email"),
#         "avatar": user.get("avatar"),
#         "bio": user.get("bio", ""),
#         "followers_count": user.get("followers_count", 0),
#         "following_count": user.get("following_count", 0),
#         "created_at": created.isoformat() if created else None
#     }


# def create_user(username: str, email: str, password_hash: bytes):
#     db = get_db()
#     doc = {
#         "username": username,
#         "email": email,
#         "password": password_hash,
#         "avatar": None,
#         "bio": "",
#         "followers_count": 0,
#         "following_count": 0,
#         "created_at": datetime.utcnow()
#     }
#     res = db.users.insert_one(doc)
#     doc["_id"] = res.inserted_id
#     return doc


# def get_user_by_email(email: str):
#     db = get_db()
#     return db.users.find_one({"email": (email or "").strip().lower()})


# def get_user_by_username(username: str):
#     db = get_db()
#     return db.users.find_one({"username": (username or "").strip()})


# def get_user_by_id(user_id: str):
#     db = get_db()
#     oid = _oid(user_id)
#     if not oid:
#         return None
#     return db.users.find_one({"_id": oid})
# from datetime import datetime
# from bson import ObjectId
# from app.extensions import get_db


# def serialize_user(u: dict) -> dict:
#     return {
#         "_id": str(u["_id"]),
#         "username": u.get("username"),
#         "email": u.get("email"),
#         "bio": u.get("bio", ""),
#         "avatar_url": u.get("avatar_url"),
#         "followers_count": u.get("followers_count", 0),
#         "following_count": u.get("following_count", 0),
#         "posts_count": u.get("posts_count", 0),
#         "created_at": u.get("created_at").isoformat() if u.get("created_at") else None,
#     }


# def create_user(username: str, email: str, password_hash: str):
#     db = get_db()
#     doc = {
#         "username": username,
#         "email": email,
#         "password_hash": password_hash,  # ✅ store here as STRING
#         "bio": "",
#         "avatar_url": None,
#         "followers_count": 0,
#         "following_count": 0,
#         "posts_count": 0,
#         "created_at": datetime.utcnow(),
#     }
#     res = db.users.insert_one(doc)
#     doc["_id"] = res.inserted_id
#     return doc


# def get_user_by_email(email: str):
#     db = get_db()
#     return db.users.find_one({"email": email})


# def get_user_by_username(username: str):
#     db = get_db()
#     return db.users.find_one({"username": username})


# def get_user_by_id(user_id: str):
#     db = get_db()
#     try:
#         return db.users.find_one({"_id": ObjectId(user_id)})
#     except Exception:
#         return None
# from bson import ObjectId
# from app.extensions import get_db

# def serialize_user(u: dict) -> dict:
#     return {
#         "_id": str(u["_id"]),
#         "username": u.get("username"),
#         "email": u.get("email"),
#         "created_at": (u.get("created_at").isoformat() if u.get("created_at") else None),
#     }

# def create_user(username: str, email: str, password_hash: str):
#     db = get_db()
#     doc = {"username": username, "email": email, "password_hash": password_hash}
#     res = db.users.insert_one(doc)
#     doc["_id"] = res.inserted_id
#     return doc

# def get_user_by_email(email: str):
#     db = get_db()
#     return db.users.find_one({"email": email})

# def get_user_by_username(username: str):
#     db = get_db()
#     return db.users.find_one({"username": username})

# def get_user_by_id(user_id: str):
#     db = get_db()
#     try:
#         return db.users.find_one({"_id": ObjectId(user_id)})
#     except Exception:
#         return None

# from flask import Blueprint, jsonify, request, g
# from bson import ObjectId
# from app.middleware.auth_required import auth_required
# from app.extensions import get_db

# user_bp = Blueprint("users", __name__, url_prefix="/api/users")


# def _oid(v):
#     try:
#         return ObjectId(str(v))
#     except Exception:
#         return None


# def _user_public(u: dict, viewer_id: str | None = None) -> dict:
#     uid = str(u.get("_id"))
#     out = {
#         "_id": uid,
#         "username": u.get("username") or "",
#         "name": u.get("name") or u.get("username") or "",
#         "bio": u.get("bio") or "",
#         "avatar_url": u.get("avatar_url") or u.get("avatarUrl") or None,
#         "postsCount": int(u.get("posts_count") or 0),
#         "followersCount": int(u.get("followers_count") or 0),
#         "followingCount": int(u.get("following_count") or 0),
#         "isFollowing": False,
#     }

#     if viewer_id:
#         db = get_db()
#         vid = _oid(viewer_id)
#         tid = _oid(uid)
#         if vid and tid:
#             out["isFollowing"] = db.follows.find_one(
#                 {"follower_id": vid, "following_id": tid}
#             ) is not None
#     return out


# @user_bp.get("/<username>")
# @auth_required
# def profile(username):
#     db = get_db()

#     # case-insensitive username match
#     u = db.users.find_one({"username": {"$regex": f"^{username}$", "$options": "i"}})
#     if not u:
#         return jsonify({"error": "User not found"}), 404

#     uid_obj = u["_id"]
#     uid_str = str(uid_obj)
#     uname = u.get("username") or username

#     # ✅ robust counts (match both author_id formats + username)
#     posts_count = db.posts.count_documents({
#         "$or": [
#             {"author_id": uid_str},
#             {"author_id": uid_obj},
#             {"author_username": {"$regex": f"^{uname}$", "$options": "i"}},
#         ]
#     })

#     followers_count = db.follows.count_documents({"following_id": uid_obj})
#     following_count = db.follows.count_documents({"follower_id": uid_obj})

#     db.users.update_one(
#         {"_id": uid_obj},
#         {"$set": {
#             "posts_count": posts_count,
#             "followers_count": followers_count,
#             "following_count": following_count
#         }},
#     )

#     u["posts_count"] = posts_count
#     u["followers_count"] = followers_count
#     u["following_count"] = following_count

#     return jsonify({"user": _user_public(u, viewer_id=str(g.user_id))}), 200


# @user_bp.get("/<username>/posts")
# @auth_required
# def user_posts(username):
#     db = get_db()

#     u = db.users.find_one({"username": {"$regex": f"^{username}$", "$options": "i"}})
#     if not u:
#         return jsonify({"error": "User not found"}), 404

#     uid_obj = u["_id"]
#     uid_str = str(uid_obj)
#     uname = u.get("username") or username

#     # ✅ THIS IS THE MAIN FIX
#     query = {
#         "$or": [
#             {"author_id": uid_str},
#             {"author_id": uid_obj},
#             {"author_username": {"$regex": f"^{uname}$", "$options": "i"}},
#         ]
#     }

#     cursor = db.posts.find(query).sort("created_at", -1).limit(60)

#     posts = []
#     for p in cursor:
#         posts.append({
#             "_id": str(p["_id"]),
#             "caption": p.get("caption") or "",
#             "media_url": p.get("media_url") or p.get("mediaUrl"),
#             "media_type": p.get("media_type") or p.get("mediaType"),
#             "created_at": p.get("created_at").isoformat() if p.get("created_at") else None,
#             "author_username": p.get("author_username"),
#         })

#     return jsonify({"posts": posts}), 200


# # ✅ NEW: list followers
# @user_bp.get("/<username>/followers")
# @auth_required
# def followers(username):
#     db = get_db()
#     u = db.users.find_one({"username": {"$regex": f"^{username}$", "$options": "i"}})
#     if not u:
#         return jsonify({"error": "User not found"}), 404

#     uid = u["_id"]

#     rels = list(db.follows.find({"following_id": uid}).limit(200))
#     follower_ids = [r.get("follower_id") for r in rels if r.get("follower_id")]

#     users = list(db.users.find({"_id": {"$in": follower_ids}}).limit(200))
#     out = [_user_public(x, viewer_id=str(g.user_id)) for x in users]

#     # keep consistent ordering (optional)
#     out.sort(key=lambda x: x.get("username", "").lower())
#     return jsonify({"users": out}), 200


# # ✅ NEW: list following
# @user_bp.get("/<username>/following")
# @auth_required
# def following(username):
#     db = get_db()
#     u = db.users.find_one({"username": {"$regex": f"^{username}$", "$options": "i"}})
#     if not u:
#         return jsonify({"error": "User not found"}), 404

#     uid = u["_id"]

#     rels = list(db.follows.find({"follower_id": uid}).limit(200))
#     following_ids = [r.get("following_id") for r in rels if r.get("following_id")]

#     users = list(db.users.find({"_id": {"$in": following_ids}}).limit(200))
#     out = [_user_public(x, viewer_id=str(g.user_id)) for x in users]
#     out.sort(key=lambda x: x.get("username", "").lower())
#     return jsonify({"users": out}), 200

# # from flask import Blueprint, jsonify, request, g
# # from bson import ObjectId
# # from app.middleware.auth_required import auth_required
# # from app.extensions import get_db

# # user_bp = Blueprint("users", __name__, url_prefix="/api/users")


# # def _oid(v):
# #     try:
# #         return ObjectId(str(v))
# #     except Exception:
# #         return None


# # def _user_public(u: dict, viewer_id: str | None = None) -> dict:
# #     uid = str(u.get("_id"))
# #     out = {
# #         "_id": uid,
# #         "username": u.get("username") or "",
# #         "name": u.get("name") or u.get("username") or "",
# #         "bio": u.get("bio") or "",
# #         "avatar_url": u.get("avatar_url") or u.get("avatarUrl") or None,
# #         "postsCount": int(u.get("posts_count") or u.get("postsCount") or 0),
# #         "followersCount": int(u.get("followers_count") or u.get("followersCount") or 0),
# #         "followingCount": int(u.get("following_count") or u.get("followingCount") or 0),
# #     }

# #     out["isFollowing"] = False
# #     if viewer_id:
# #         db = get_db()
# #         vid = _oid(viewer_id)
# #         tid = _oid(uid)
# #         if vid and tid:
# #             out["isFollowing"] = db.follows.find_one(
# #                 {"follower_id": vid, "following_id": tid}
# #             ) is not None

# #     return out


# # def _author_match(user_oid: ObjectId):
# #     """
# #     IMPORTANT FIX:
# #     posts.author_id in your DB may be ObjectId OR string.
# #     This matcher supports both.
# #     """
# #     return {"$or": [{"author_id": user_oid}, {"author_id": str(user_oid)}]}


# # @user_bp.get("/me")
# # @auth_required
# # def me():
# #     db = get_db()
# #     uid = _oid(g.user_id)
# #     if not uid:
# #         return jsonify({"error": "Invalid user id"}), 400

# #     u = db.users.find_one({"_id": uid})
# #     if not u:
# #         return jsonify({"error": "User not found"}), 404

# #     # sync counts
# #     posts_count = db.posts.count_documents(_author_match(uid))
# #     followers_count = db.follows.count_documents({"following_id": uid})
# #     following_count = db.follows.count_documents({"follower_id": uid})

# #     db.users.update_one(
# #         {"_id": uid},
# #         {"$set": {"posts_count": posts_count, "followers_count": followers_count, "following_count": following_count}},
# #     )

# #     u["posts_count"] = posts_count
# #     u["followers_count"] = followers_count
# #     u["following_count"] = following_count

# #     return jsonify({"user": _user_public(u, viewer_id=str(g.user_id))}), 200


# # @user_bp.get("/<username>")
# # @auth_required
# # def profile(username):
# #     db = get_db()
# #     u = db.users.find_one({"username": username})
# #     if not u:
# #         return jsonify({"error": "User not found"}), 404

# #     uid = u["_id"]

# #     # sync counts using FIXED matcher
# #     posts_count = db.posts.count_documents(_author_match(uid))
# #     followers_count = db.follows.count_documents({"following_id": uid})
# #     following_count = db.follows.count_documents({"follower_id": uid})

# #     db.users.update_one(
# #         {"_id": uid},
# #         {"$set": {"posts_count": posts_count, "followers_count": followers_count, "following_count": following_count}},
# #     )

# #     u["posts_count"] = posts_count
# #     u["followers_count"] = followers_count
# #     u["following_count"] = following_count

# #     return jsonify({"user": _user_public(u, viewer_id=str(g.user_id))}), 200


# # @user_bp.get("/<username>/posts")
# # @auth_required
# # def user_posts(username):
# #     db = get_db()
# #     u = db.users.find_one({"username": username})
# #     if not u:
# #         return jsonify({"error": "User not found"}), 404

# #     uid = u["_id"]

# #     cursor = db.posts.find(_author_match(uid)).sort("created_at", -1).limit(60)

# #     posts = []
# #     for p in cursor:
# #         posts.append(
# #             {
# #                 "_id": str(p["_id"]),
# #                 "caption": p.get("caption") or "",
# #                 "media_url": p.get("media_url") or p.get("mediaUrl"),
# #                 "media_type": p.get("media_type") or p.get("mediaType"),
# #                 "created_at": p.get("created_at").isoformat() if p.get("created_at") else None,
# #             }
# #         )
# #     return jsonify({"posts": posts}), 200


# # @user_bp.get("/suggestions")
# # @auth_required
# # def suggestions():
# #     db = get_db()
# #     limit = int(request.args.get("limit") or 6)

# #     viewer_oid = _oid(g.user_id)
# #     if not viewer_oid:
# #         return jsonify({"error": "Invalid viewer id"}), 400

# #     following_ids = list(db.follows.find({"follower_id": viewer_oid}, {"following_id": 1}))
# #     following_set = {x["following_id"] for x in following_ids}

# #     pipeline = [
# #         {"$match": {"_id": {"$ne": viewer_oid, "$nin": list(following_set)}}},
# #         {"$addFields": {"posts_count": {"$ifNull": ["$posts_count", 0]}}},
# #         {"$sort": {"posts_count": -1}},
# #         {"$limit": max(limit * 3, 20)},
# #     ]

# #     candidates = list(db.users.aggregate(pipeline))
# #     out = [_user_public(u, viewer_id=str(g.user_id)) for u in candidates[:limit]]
# #     return jsonify({"users": out}), 200


# # # -------------------- FOLLOW LISTS (NEW) --------------------

# # @user_bp.get("/<username>/followers")
# # @auth_required
# # def followers(username):
# #     db = get_db()
# #     u = db.users.find_one({"username": username})
# #     if not u:
# #         return jsonify({"error": "User not found"}), 404

# #     uid = u["_id"]
# #     limit = min(int(request.args.get("limit") or 50), 100)
# #     skip = max(int(request.args.get("skip") or 0), 0)

# #     rel = list(
# #         db.follows.find({"following_id": uid})
# #         .sort("created_at", -1)
# #         .skip(skip)
# #         .limit(limit)
# #     )

# #     follower_ids = [r.get("follower_id") for r in rel if r.get("follower_id")]
# #     users = list(db.users.find({"_id": {"$in": follower_ids}}))

# #     users_by_id = {str(x["_id"]): x for x in users}
# #     out = []
# #     for fid in follower_ids:
# #         x = users_by_id.get(str(fid))
# #         if x:
# #             out.append(_user_public(x, viewer_id=str(g.user_id)))

# #     return jsonify({"users": out}), 200


# # @user_bp.get("/<username>/following")
# # @auth_required
# # def following(username):
# #     db = get_db()
# #     u = db.users.find_one({"username": username})
# #     if not u:
# #         return jsonify({"error": "User not found"}), 404

# #     uid = u["_id"]
# #     limit = min(int(request.args.get("limit") or 50), 100)
# #     skip = max(int(request.args.get("skip") or 0), 0)

# #     rel = list(
# #         db.follows.find({"follower_id": uid})
# #         .sort("created_at", -1)
# #         .skip(skip)
# #         .limit(limit)
# #     )

# #     following_ids = [r.get("following_id") for r in rel if r.get("following_id")]
# #     users = list(db.users.find({"_id": {"$in": following_ids}}))

# #     users_by_id = {str(x["_id"]): x for x in users}
# #     out = []
# #     for fid in following_ids:
# #         x = users_by_id.get(str(fid))
# #         if x:
# #             out.append(_user_public(x, viewer_id=str(g.user_id)))

# #     return jsonify({"users": out}), 200

# # app/models/user_model.py
# from datetime import datetime
# from bson import ObjectId
# from app.extensions import get_db, hash_password, check_password


# def _oid(v):
#     try:
#         return ObjectId(str(v))
#     except Exception:
#         return None


# def create_user(username: str, password: str, name: str | None = None, bio: str = "") -> dict:
#     """
#     Creates a new user in db.users
#     - stores password_hash
#     - initializes counts
#     """
#     db = get_db()
#     username = (username or "").strip()

#     if not username or not password:
#         raise ValueError("username and password are required")

#     # unique username
#     exists = db.users.find_one({"username": username})
#     if exists:
#         raise ValueError("Username already exists")

#     doc = {
#         "username": username,
#         "name": name or username,
#         "bio": bio or "",
#         "avatar_url": None,
#         "password_hash": hash_password(password),
#         "posts_count": 0,
#         "followers_count": 0,
#         "following_count": 0,
#         "created_at": datetime.utcnow(),
#         "updated_at": datetime.utcnow(),
#     }

#     res = db.users.insert_one(doc)
#     doc["_id"] = res.inserted_id
#     return doc


# def get_user_by_username(username: str) -> dict | None:
#     db = get_db()
#     return db.users.find_one({"username": username})


# def get_user_by_id(user_id: str) -> dict | None:
#     db = get_db()
#     oid = _oid(user_id)
#     if not oid:
#         return None
#     return db.users.find_one({"_id": oid})


# def verify_password(user: dict, password: str) -> bool:
#     """
#     Checks provided password against password_hash in DB user doc
#     """
#     if not user:
#         return False
#     return check_password(password, user.get("password_hash") or "")


# def serialize_user_public(u: dict) -> dict:
#     """
#     Safe payload for frontend
#     """
#     if not u:
#         return {}

#     return {
#         "_id": str(u.get("_id")),
#         "username": u.get("username") or "",
#         "name": u.get("name") or u.get("username") or "",
#         "bio": u.get("bio") or "",
#         "avatar_url": u.get("avatar_url") or u.get("avatarUrl") or None,
#         "postsCount": int(u.get("posts_count") or 0),
#         "followersCount": int(u.get("followers_count") or 0),
#         "followingCount": int(u.get("following_count") or 0),
#         "created_at": u.get("created_at").isoformat() if u.get("created_at") else None,
#     }

# app/models/user_model.py
from datetime import datetime
from bson import ObjectId
from app.extensions import get_db, hash_password, check_password


def _oid(v):
    try:
        return ObjectId(str(v))
    except Exception:
        return None


def create_user(
    username: str,
    password: str,
    email: str | None = None,
    name: str | None = None,
    bio: str = "",
) -> dict:
    """
    Creates a new user in db.users
    - stores password_hash
    - initializes counts
    - supports email (optional)
    """
    db = get_db()

    username = (username or "").strip().lower()
    email = (email or "").strip().lower() if email else None

    if not username or not password:
        raise ValueError("username and password are required")

    # unique username
    if db.users.find_one({"username": username}):
        raise ValueError("Username already exists")

    # unique email (if provided)
    if email and db.users.find_one({"email": email}):
        raise ValueError("Email already exists")

    doc = {
        "username": username,
        "email": email,  # ✅ add email field
        "name": name or username,
        "bio": bio or "",
        "website": "",
        "avatar_url": None,
        "password_hash": hash_password(password),
        "posts_count": 0,
        "followers_count": 0,
        "following_count": 0,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }

    res = db.users.insert_one(doc)
    doc["_id"] = res.inserted_id
    return doc


def get_user_by_username(username: str) -> dict | None:
    db = get_db()
    if not username:
        return None
    return db.users.find_one({"username": username.strip().lower()})


def get_user_by_email(email: str) -> dict | None:
    """✅ FIX: Auth routes need this"""
    db = get_db()
    if not email:
        return None
    return db.users.find_one({"email": email.strip().lower()})


def get_user_by_id(user_id: str) -> dict | None:
    db = get_db()
    oid = _oid(user_id)
    if not oid:
        return None
    return db.users.find_one({"_id": oid})


def verify_password(user: dict, password: str) -> bool:
    if not user:
        return False
    return check_password(password, user.get("password_hash") or "")


def serialize_user_public(u: dict) -> dict:
    if not u:
        return {}

    return {
        "_id": str(u.get("_id")),
        "username": u.get("username") or "",
        "email": u.get("email") or None,
        "name": u.get("name") or u.get("username") or "",
        "bio": u.get("bio") or "",
        "website": u.get("website") or "",
        "avatar_url": u.get("avatar_url") or u.get("avatarUrl") or None,
        "postsCount": int(u.get("posts_count") or 0),
        "followersCount": int(u.get("followers_count") or 0),
        "followingCount": int(u.get("following_count") or 0),
        "created_at": u.get("created_at").isoformat() if u.get("created_at") else None,
    }


# ✅ FIX: auth_routes imports serialize_user (old name)
def serialize_user(u: dict) -> dict:
    return serialize_user_public(u)