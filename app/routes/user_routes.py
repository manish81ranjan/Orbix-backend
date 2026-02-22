# """
# User model helpers (MongoDB)
# """

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


# def update_user(user_id: str, updates: dict):
#     db = get_db()
#     oid = _oid(user_id)
#     if not oid:
#         raise ValueError("Invalid user_id")

#     updates = updates or {}
#     allowed = {"username", "avatar", "bio"}
#     clean = {k: v for k, v in updates.items() if k in allowed}

#     if not clean:
#         return None

#     db.users.update_one({"_id": oid}, {"$set": clean})
#     return db.users.find_one({"_id": oid})
# from flask import Blueprint, jsonify, request

# user_bp = Blueprint("users", __name__)

# @user_bp.get("/")
# def users_root():
#     return jsonify({"message": "Users blueprint working"}), 200


# @user_bp.get("/<user_id>")
# def get_user(user_id):
#     # ✅ import inside function prevents import-time crashes
#     from app.models.user_model import get_user_by_id, serialize_user

#     user = get_user_by_id(user_id)
#     if not user:
#         return jsonify({"error": "User not found"}), 404
#     return jsonify({"user": serialize_user(user)}), 200


# @user_bp.get("/username/<username>")
# def get_by_username(username):
#     from app.models.user_model import get_user_by_username, serialize_user

#     user = get_user_by_username(username)
#     if not user:
#         return jsonify({"error": "User not found"}), 404
#     return jsonify({"user": serialize_user(user)}), 200


# @user_bp.patch("/<user_id>")
# def patch_user(user_id):
#     from app.models.user_model import update_user, serialize_user

#     updates = request.get_json(silent=True)
#     if updates is None:
#         return jsonify({"error": "Invalid or missing JSON body"}), 400

#     try:
#         user = update_user(user_id, updates)
#     except ValueError as e:
#         return jsonify({"error": str(e)}), 400

#     if not user:
#         return jsonify({"error": "No valid fields to update"}), 400

#     return jsonify({"user": serialize_user(user)}), 200
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
#     """
#     Public user payload (safe)
#     """
#     uid = str(u.get("_id"))
#     out = {
#         "_id": uid,
#         "username": u.get("username") or "",
#         "name": u.get("name") or u.get("username") or "",
#         "bio": u.get("bio") or "",
#         "avatar_url": u.get("avatar_url") or u.get("avatarUrl") or None,
#         "postsCount": int(u.get("posts_count") or u.get("postsCount") or 0),
#         "followersCount": int(u.get("followers_count") or u.get("followersCount") or 0),
#         "followingCount": int(u.get("following_count") or u.get("followingCount") or 0),
#     }

#     # isFollowing (viewer -> this user)
#     out["isFollowing"] = False
#     if viewer_id:
#         db = get_db()
#         vid = _oid(viewer_id)
#         tid = _oid(uid)
#         if vid and tid:
#             out["isFollowing"] = db.follows.find_one({"follower_id": vid, "following_id": tid}) is not None

#     return out


# @user_bp.get("/me")
# @auth_required
# def me():
#     db = get_db()
#     uid = _oid(g.user_id)
#     if not uid:
#         return jsonify({"error": "Invalid user id"}), 400

#     u = db.users.find_one({"_id": uid})
#     if not u:
#         return jsonify({"error": "User not found"}), 404

#     return jsonify({"user": _user_public(u, viewer_id=str(g.user_id))}), 200


# @user_bp.get("/<username>")
# @auth_required
# def profile(username):
#     db = get_db()
#     u = db.users.find_one({"username": username})
#     if not u:
#         return jsonify({"error": "User not found"}), 404

#     # Keep counts synced from DB if needed (fallback)
#     uid = u["_id"]
#     posts_count = db.posts.count_documents({"author_id": str(uid)})
#     followers_count = db.follows.count_documents({"following_id": uid})
#     following_count = db.follows.count_documents({"follower_id": uid})

#     db.users.update_one(
#         {"_id": uid},
#         {"$set": {"posts_count": posts_count, "followers_count": followers_count, "following_count": following_count}},
#     )

#     # re-read minimal fields
#     u["posts_count"] = posts_count
#     u["followers_count"] = followers_count
#     u["following_count"] = following_count

#     return jsonify({"user": _user_public(u, viewer_id=str(g.user_id))}), 200


# @user_bp.get("/<username>/posts")
# @auth_required
# def user_posts(username):
#     db = get_db()
#     u = db.users.find_one({"username": username})
#     if not u:
#         return jsonify({"error": "User not found"}), 404

#     uid = str(u["_id"])

#     # Only posts with media for grid (like Instagram)
#     cursor = db.posts.find({"author_id": uid}).sort("created_at", -1).limit(60)

#     posts = []
#     for p in cursor:
#         posts.append(
#             {
#                 "_id": str(p["_id"]),
#                 "caption": p.get("caption") or "",
#                 "media_url": p.get("media_url"),
#                 "media_type": p.get("media_type"),
#                 "created_at": p.get("created_at").isoformat() if p.get("created_at") else None,
#             }
#         )
#     return jsonify({"posts": posts}), 200


# @user_bp.get("/suggestions")
# @auth_required
# def suggestions():
#     """
#     Real suggestions:
#     - not you
#     - not already followed
#     - limit= (default 6)
#     """
#     db = get_db()
#     limit = int(request.args.get("limit") or 6)

#     viewer_oid = _oid(g.user_id)
#     if not viewer_oid:
#         return jsonify({"error": "Invalid viewer id"}), 400

#     # who am I already following?
#     following_ids = list(
#         db.follows.find({"follower_id": viewer_oid}, {"following_id": 1})
#     )
#     following_set = {x["following_id"] for x in following_ids}

#     # candidates: all users except me & already-followed
#     pipeline = [
#         {"$match": {"_id": {"$ne": viewer_oid, "$nin": list(following_set)}}},
#         # Optional: prioritize active users (most posts)
#         {"$addFields": {"posts_count": {"$ifNull": ["$posts_count", 0]}}},
#         {"$sort": {"posts_count": -1}},
#         {"$limit": max(limit * 3, 20)},
#     ]

#     candidates = list(db.users.aggregate(pipeline))

#     # small shuffle for variety
#     # (keep stable-ish but not same list always)
#     out = [_user_public(u, viewer_id=str(g.user_id)) for u in candidates[:limit]]

#     return jsonify({"users": out}), 200
# from datetime import datetime
# from typing import Optional

# from flask import Blueprint, jsonify, request, g
# from bson import ObjectId
# from werkzeug.security import generate_password_hash, check_password_hash

# from app.middleware.auth_required import auth_required
# from app.extensions import get_db
# from app.models.user_model import create_user, get_user_by_username, verify_password, serialize_user_public
# # from app.extensions import get_db
# user_bp = Blueprint("users", __name__, url_prefix="/api/users")


# # -------------------------
# # helpers
# # -------------------------
# def _oid(v):
#     try:
#         return ObjectId(str(v))
#     except Exception:
#         return None


# def _safe_int(v, default=0):
#     try:
#         return int(v)
#     except Exception:
#         return default


# def _user_public(u: dict, viewer_id: Optional[str] = None) -> dict:
#     """
#     Public user payload (safe)
#     """
#     uid = str(u.get("_id"))
#     out = {
#         "_id": uid,
#         "username": u.get("username") or "",
#         "name": u.get("name") or u.get("username") or "",
#         "bio": u.get("bio") or "",
#         "website": u.get("website") or "",
#         "avatar_url": u.get("avatar_url") or u.get("avatarUrl") or None,
#         "postsCount": _safe_int(u.get("posts_count") or u.get("postsCount") or 0),
#         "followersCount": _safe_int(u.get("followers_count") or u.get("followersCount") or 0),
#         "followingCount": _safe_int(u.get("following_count") or u.get("followingCount") or 0),
#     }

#     # isFollowing (viewer -> this user)
#     out["isFollowing"] = False
#     if viewer_id:
#         db = get_db()
#         vid = _oid(viewer_id)
#         tid = _oid(uid)
#         if vid and tid:
#             out["isFollowing"] = (
#                 db.follows.find_one({"follower_id": vid, "following_id": tid}) is not None
#             )

#     return out


# def _sync_user_counts(db, user_oid: ObjectId):
#     """
#     Keep counters consistent (posts_count, followers_count, following_count)
#     NOTE:
#     - posts.author_id is stored as STRING of user id
#     - follows uses ObjectId references
#     """
#     uid_str = str(user_oid)

#     posts_count = db.posts.count_documents({"author_id": uid_str})
#     followers_count = db.follows.count_documents({"following_id": user_oid})
#     following_count = db.follows.count_documents({"follower_id": user_oid})

#     db.users.update_one(
#         {"_id": user_oid},
#         {"$set": {
#             "posts_count": posts_count,
#             "followers_count": followers_count,
#             "following_count": following_count
#         }},
#     )

#     return posts_count, followers_count, following_count


# # -------------------------
# # ME (profile of logged-in user)
# # -------------------------
# @user_bp.get("/me")
# @auth_required
# def me():
#     db = get_db()
#     uid = _oid(g.user_id)
#     if not uid:
#         return jsonify({"error": "Invalid user id"}), 400

#     u = db.users.find_one({"_id": uid})
#     if not u:
#         return jsonify({"error": "User not found"}), 404

#     # keep counts fresh
#     posts_count, followers_count, following_count = _sync_user_counts(db, uid)
#     u["posts_count"] = posts_count
#     u["followers_count"] = followers_count
#     u["following_count"] = following_count

#     return jsonify({"user": _user_public(u, viewer_id=str(g.user_id))}), 200


# # -------------------------
# # UPDATE ME (Settings -> Edit Profile)
# # PATCH /api/users/me
# # -------------------------
# @user_bp.patch("/me")
# @auth_required
# def update_me():
#     db = get_db()
#     uid = _oid(g.user_id)
#     if not uid:
#         return jsonify({"error": "Invalid user id"}), 400

#     data = request.get_json(silent=True) or {}

#     name = (data.get("name") or "").strip()
#     bio = (data.get("bio") or "").strip()
#     website = (data.get("website") or "").strip()
#     avatar_url = (data.get("avatar_url") or data.get("avatarUrl") or "").strip()

#     update = {}
#     if name != "":
#         update["name"] = name
#     if bio != "":
#         update["bio"] = bio
#     if website != "":
#         update["website"] = website
#     if avatar_url != "":
#         update["avatar_url"] = avatar_url

#     if not update:
#         return jsonify({"error": "Nothing to update"}), 400

#     db.users.update_one({"_id": uid}, {"$set": update})

#     u = db.users.find_one({"_id": uid})
#     return jsonify({"user": _user_public(u, viewer_id=str(g.user_id))}), 200


# # -------------------------
# # CHANGE PASSWORD (Settings -> Password)
# # POST /api/users/change-password
# # body: { currentPassword, newPassword }
# # -------------------------
# @user_bp.post("/change-password")
# @auth_required
# def change_password():
#     db = get_db()
#     uid = _oid(g.user_id)
#     if not uid:
#         return jsonify({"error": "Invalid user id"}), 400

#     data = request.get_json(silent=True) or {}
#     current_pw = data.get("currentPassword") or data.get("current") or ""
#     new_pw = data.get("newPassword") or data.get("next") or ""

#     current_pw = str(current_pw)
#     new_pw = str(new_pw)

#     if len(new_pw) < 6:
#         return jsonify({"error": "New password must be at least 6 characters"}), 400

#     u = db.users.find_one({"_id": uid})
#     if not u:
#         return jsonify({"error": "User not found"}), 404

#     pw_hash = u.get("password_hash") or u.get("passwordHash")
#     if not pw_hash:
#         return jsonify({"error": "Password hash missing for this user"}), 400

#     if not check_password_hash(pw_hash, current_pw):
#         return jsonify({"error": "Current password is incorrect"}), 400

#     db.users.update_one(
#         {"_id": uid},
#         {"$set": {"password_hash": generate_password_hash(new_pw), "updated_at": datetime.utcnow()}},
#     )

#     return jsonify({"ok": True}), 200


# # -------------------------
# # PUBLIC PROFILE
# # -------------------------
# @user_bp.get("/<username>")
# @auth_required
# def profile(username):
#     db = get_db()
#     u = db.users.find_one({"username": username})
#     if not u:
#         return jsonify({"error": "User not found"}), 404

#     user_oid = u["_id"]
#     posts_count, followers_count, following_count = _sync_user_counts(db, user_oid)

#     u["posts_count"] = posts_count
#     u["followers_count"] = followers_count
#     u["following_count"] = following_count

#     return jsonify({"user": _user_public(u, viewer_id=str(g.user_id))}), 200


# # -------------------------
# # USER POSTS (profile grid)
# # NOTE: posts.author_id is STRING
# # -------------------------
# @user_bp.get("/<username>/posts")
# @auth_required
# def user_posts(username):
#     db = get_db()
#     u = db.users.find_one({"username": username})
#     if not u:
#         return jsonify({"error": "User not found"}), 404

#     uid_str = str(u["_id"])

#     cursor = db.posts.find({"author_id": uid_str}).sort("created_at", -1).limit(60)

#     posts = []
#     for p in cursor:
#         posts.append(
#             {
#                 "_id": str(p["_id"]),
#                 "caption": p.get("caption") or "",
#                 "media_url": p.get("media_url"),
#                 "media_type": p.get("media_type"),
#                 "created_at": p.get("created_at").isoformat() if p.get("created_at") else None,
#             }
#         )

#     return jsonify({"posts": posts}), 200


# # -------------------------
# # FOLLOWERS LIST (Instagram-style)
# # GET /api/users/<username>/followers?limit=20&skip=0
# # -------------------------
# @user_bp.get("/<username>/followers")
# @auth_required
# def followers(username):
#     db = get_db()
#     u = db.users.find_one({"username": username})
#     if not u:
#         return jsonify({"error": "User not found"}), 404

#     limit = min(int(request.args.get("limit") or 20), 50)
#     skip = max(int(request.args.get("skip") or 0), 0)

#     user_oid = u["_id"]

#     # followers are: follows where following_id = this user
#     cursor = db.follows.find({"following_id": user_oid}).skip(skip).limit(limit)

#     follower_ids = [x.get("follower_id") for x in cursor if x.get("follower_id")]
#     if not follower_ids:
#         return jsonify({"users": []}), 200

#     users = list(db.users.find({"_id": {"$in": follower_ids}}))
#     # keep same order
#     by_id = {str(x["_id"]): x for x in users}
#     out = []
#     for oid in follower_ids:
#         uu = by_id.get(str(oid))
#         if uu:
#             out.append(_user_public(uu, viewer_id=str(g.user_id)))

#     return jsonify({"users": out}), 200


# # -------------------------
# # FOLLOWING LIST
# # GET /api/users/<username>/following?limit=20&skip=0
# # -------------------------
# @user_bp.get("/<username>/following")
# @auth_required
# def following(username):
#     db = get_db()
#     u = db.users.find_one({"username": username})
#     if not u:
#         return jsonify({"error": "User not found"}), 404

#     limit = min(int(request.args.get("limit") or 20), 50)
#     skip = max(int(request.args.get("skip") or 0), 0)

#     user_oid = u["_id"]

#     # following are: follows where follower_id = this user
#     cursor = db.follows.find({"follower_id": user_oid}).skip(skip).limit(limit)

#     following_ids = [x.get("following_id") for x in cursor if x.get("following_id")]
#     if not following_ids:
#         return jsonify({"users": []}), 200

#     users = list(db.users.find({"_id": {"$in": following_ids}}))
#     by_id = {str(x["_id"]): x for x in users}
#     out = []
#     for oid in following_ids:
#         uu = by_id.get(str(oid))
#         if uu:
#             out.append(_user_public(uu, viewer_id=str(g.user_id)))

#     return jsonify({"users": out}), 200


# # -------------------------
# # BLOCK SYSTEM (Settings -> Blocked)
# # blocks collection:
# # { blocker_id: ObjectId, blocked_id: ObjectId, created_at: datetime }
# # -------------------------
# @user_bp.get("/blocked")
# @auth_required
# def blocked_list():
#     db = get_db()
#     viewer_oid = _oid(g.user_id)
#     if not viewer_oid:
#         return jsonify({"error": "Invalid viewer id"}), 400

#     cursor = db.blocks.find({"blocker_id": viewer_oid}).sort("created_at", -1).limit(200)
#     blocked_ids = [x.get("blocked_id") for x in cursor if x.get("blocked_id")]
#     if not blocked_ids:
#         return jsonify({"users": []}), 200

#     users = list(db.users.find({"_id": {"$in": blocked_ids}}))
#     by_id = {str(x["_id"]): x for x in users}
#     out = []
#     for oid in blocked_ids:
#         uu = by_id.get(str(oid))
#         if uu:
#             out.append(_user_public(uu, viewer_id=str(g.user_id)))

#     return jsonify({"users": out}), 200


# @user_bp.post("/block")
# @auth_required
# def block_user():
#     db = get_db()
#     viewer_oid = _oid(g.user_id)
#     if not viewer_oid:
#         return jsonify({"error": "Invalid viewer id"}), 400

#     data = request.get_json(silent=True) or {}
#     username = (data.get("username") or "").strip()
#     if not username:
#         return jsonify({"error": "username required"}), 400

#     u = db.users.find_one({"username": username})
#     if not u:
#         return jsonify({"error": "User not found"}), 404

#     target_oid = u["_id"]
#     if target_oid == viewer_oid:
#         return jsonify({"error": "You cannot block yourself"}), 400

#     exists = db.blocks.find_one({"blocker_id": viewer_oid, "blocked_id": target_oid})
#     if not exists:
#         db.blocks.insert_one({"blocker_id": viewer_oid, "blocked_id": target_oid, "created_at": datetime.utcnow()})

#     # optional: unfollow each other when blocked
#     db.follows.delete_many({"follower_id": viewer_oid, "following_id": target_oid})
#     db.follows.delete_many({"follower_id": target_oid, "following_id": viewer_oid})

#     return jsonify({"ok": True}), 200


# @user_bp.post("/unblock")
# @auth_required
# def unblock_user():
#     db = get_db()
#     viewer_oid = _oid(g.user_id)
#     if not viewer_oid:
#         return jsonify({"error": "Invalid viewer id"}), 400

#     data = request.get_json(silent=True) or {}
#     username = (data.get("username") or "").strip()
#     if not username:
#         return jsonify({"error": "username required"}), 400

#     u = db.users.find_one({"username": username})
#     if not u:
#         return jsonify({"error": "User not found"}), 404

#     target_oid = u["_id"]
#     db.blocks.delete_one({"blocker_id": viewer_oid, "blocked_id": target_oid})

#     return jsonify({"ok": True}), 200


# # -------------------------
# # SUGGESTIONS (real)
# # - not you
# # - not already followed
# # - not blocked by you
# # - not blocking you
# # GET /api/users/suggestions?limit=6
# # -------------------------
# @user_bp.get("/suggestions")
# @auth_required
# def suggestions():
#     db = get_db()
#     limit = min(int(request.args.get("limit") or 6), 20)

#     viewer_oid = _oid(g.user_id)
#     if not viewer_oid:
#         return jsonify({"error": "Invalid viewer id"}), 400

#     # already following
#     following_docs = list(db.follows.find({"follower_id": viewer_oid}, {"following_id": 1}))
#     following_set = {x["following_id"] for x in following_docs if x.get("following_id")}

#     # blocks: who I blocked
#     my_blocks = list(db.blocks.find({"blocker_id": viewer_oid}, {"blocked_id": 1}))
#     blocked_set = {x["blocked_id"] for x in my_blocks if x.get("blocked_id")}

#     # blocks: who blocked me
#     blocked_me = list(db.blocks.find({"blocked_id": viewer_oid}, {"blocker_id": 1}))
#     blocked_me_set = {x["blocker_id"] for x in blocked_me if x.get("blocker_id")}

#     exclude = set([viewer_oid]) | following_set | blocked_set | blocked_me_set

#     pipeline = [
#         {"$match": {"_id": {"$nin": list(exclude)}}},
#         {"$addFields": {"posts_count": {"$ifNull": ["$posts_count", 0]}}},
#         {"$sort": {"posts_count": -1, "followers_count": -1}},
#         {"$limit": max(limit * 3, 20)},
#     ]

#     candidates = list(db.users.aggregate(pipeline))
#     out = [_user_public(u, viewer_id=str(g.user_id)) for u in candidates[:limit]]

#     return jsonify({"users": out}), 200

# from datetime import datetime
# from typing import Optional

# from flask import Blueprint, jsonify, request, g
# from bson import ObjectId
# from werkzeug.security import generate_password_hash, check_password_hash

# from app.middleware.auth_required import auth_required
# from app.extensions import get_db

# user_bp = Blueprint("users", __name__, url_prefix="/api/users")


# def _oid(v):
#     try:
#         return ObjectId(str(v))
#     except Exception:
#         return None


# def _safe_int(v, default=0):
#     try:
#         return int(v)
#     except Exception:
#         return default


# def _user_public(u: dict, viewer_id: Optional[str] = None) -> dict:
#     uid = str(u.get("_id"))
#     out = {
#         "_id": uid,
#         "username": u.get("username") or "",
#         "name": u.get("name") or u.get("username") or "",
#         "bio": u.get("bio") or "",
#         "website": u.get("website") or "",
#         "avatar_url": u.get("avatar_url") or u.get("avatarUrl") or None,
#         "postsCount": _safe_int(u.get("posts_count") or u.get("postsCount") or 0),
#         "followersCount": _safe_int(u.get("followers_count") or u.get("followersCount") or 0),
#         "followingCount": _safe_int(u.get("following_count") or u.get("followingCount") or 0),
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


# def _sync_user_counts(db, user_oid: ObjectId):
#     """
#     posts.author_id = STRING of user_id
#     follows use ObjectId references
#     """
#     uid_str = str(user_oid)

#     posts_count = db.posts.count_documents({"author_id": uid_str})
#     followers_count = db.follows.count_documents({"following_id": user_oid})
#     following_count = db.follows.count_documents({"follower_id": user_oid})

#     db.users.update_one(
#         {"_id": user_oid},
#         {"$set": {
#             "posts_count": posts_count,
#             "followers_count": followers_count,
#             "following_count": following_count,
#             "updated_at": datetime.utcnow(),
#         }},
#     )

#     return posts_count, followers_count, following_count


# # -------------------------
# # ME
# # -------------------------
# @user_bp.get("/me")
# @auth_required
# def me():
#     db = get_db()
#     uid = _oid(g.user_id)
#     if not uid:
#         return jsonify({"error": "Invalid user id"}), 400

#     u = db.users.find_one({"_id": uid})
#     if not u:
#         return jsonify({"error": "User not found"}), 404

#     posts_count, followers_count, following_count = _sync_user_counts(db, uid)
#     u["posts_count"] = posts_count
#     u["followers_count"] = followers_count
#     u["following_count"] = following_count

#     return jsonify({"user": _user_public(u, viewer_id=str(g.user_id))}), 200


# # -------------------------
# # UPDATE ME
# # -------------------------
# @user_bp.patch("/me")
# @auth_required
# def update_me():
#     db = get_db()
#     uid = _oid(g.user_id)
#     if not uid:
#         return jsonify({"error": "Invalid user id"}), 400

#     data = request.get_json(silent=True) or {}

#     name = (data.get("name") or "").strip()
#     bio = (data.get("bio") or "").strip()
#     website = (data.get("website") or "").strip()
#     avatar_url = (data.get("avatar_url") or data.get("avatarUrl") or "").strip()

#     update = {}
#     if name != "":
#         update["name"] = name
#     if bio != "":
#         update["bio"] = bio
#     if website != "":
#         update["website"] = website
#     if avatar_url != "":
#         update["avatar_url"] = avatar_url

#     if not update:
#         return jsonify({"error": "Nothing to update"}), 400

#     update["updated_at"] = datetime.utcnow()
#     db.users.update_one({"_id": uid}, {"$set": update})

#     u = db.users.find_one({"_id": uid})
#     return jsonify({"user": _user_public(u, viewer_id=str(g.user_id))}), 200


# # -------------------------
# # CHANGE PASSWORD
# # -------------------------
# @user_bp.post("/change-password")
# @auth_required
# def change_password():
#     db = get_db()
#     uid = _oid(g.user_id)
#     if not uid:
#         return jsonify({"error": "Invalid user id"}), 400

#     data = request.get_json(silent=True) or {}
#     current_pw = str(data.get("currentPassword") or data.get("current") or "")
#     new_pw = str(data.get("newPassword") or data.get("next") or "")

#     if len(new_pw) < 6:
#         return jsonify({"error": "New password must be at least 6 characters"}), 400

#     u = db.users.find_one({"_id": uid})
#     if not u:
#         return jsonify({"error": "User not found"}), 404

#     pw_hash = u.get("password_hash") or u.get("passwordHash")
#     if not pw_hash:
#         return jsonify({"error": "Password hash missing for this user"}), 400

#     if not check_password_hash(pw_hash, current_pw):
#         return jsonify({"error": "Current password is incorrect"}), 400

#     db.users.update_one(
#         {"_id": uid},
#         {"$set": {"password_hash": generate_password_hash(new_pw), "updated_at": datetime.utcnow()}},
#     )

#     return jsonify({"ok": True}), 200


# # -------------------------
# # PUBLIC PROFILE
# # -------------------------
# @user_bp.get("/<username>")
# @auth_required
# def profile(username):
#     db = get_db()
#     u = db.users.find_one({"username": username})
#     if not u:
#         return jsonify({"error": "User not found"}), 404

#     user_oid = u["_id"]
#     posts_count, followers_count, following_count = _sync_user_counts(db, user_oid)

#     u["posts_count"] = posts_count
#     u["followers_count"] = followers_count
#     u["following_count"] = following_count

#     return jsonify({"user": _user_public(u, viewer_id=str(g.user_id))}), 200


# # -------------------------
# # PROFILE POSTS GRID
# # -------------------------
# @user_bp.get("/<username>/posts")
# @auth_required
# def user_posts(username):
#     db = get_db()
#     u = db.users.find_one({"username": username})
#     if not u:
#         return jsonify({"error": "User not found"}), 404

#     uid_str = str(u["_id"])

#     cursor = db.posts.find({"author_id": uid_str}).sort("created_at", -1).limit(60)

#     posts = []
#     for p in cursor:
#         posts.append(
#             {
#                 "_id": str(p["_id"]),
#                 "caption": p.get("caption") or "",
#                 "media_url": p.get("media_url"),
#                 "media_type": p.get("media_type"),
#                 "created_at": p.get("created_at").isoformat() if p.get("created_at") else None,
#             }
#         )

#     return jsonify({"posts": posts}), 200


# # -------------------------
# # FOLLOWERS LIST
# # -------------------------
# @user_bp.get("/<username>/followers")
# @auth_required
# def followers(username):
#     db = get_db()
#     u = db.users.find_one({"username": username})
#     if not u:
#         return jsonify({"error": "User not found"}), 404

#     limit = min(int(request.args.get("limit") or 20), 50)
#     skip = max(int(request.args.get("skip") or 0), 0)

#     user_oid = u["_id"]

#     cursor = db.follows.find({"following_id": user_oid}).skip(skip).limit(limit)
#     follower_ids = [x.get("follower_id") for x in cursor if x.get("follower_id")]

#     if not follower_ids:
#         return jsonify({"users": []}), 200

#     users = list(db.users.find({"_id": {"$in": follower_ids}}))
#     by_id = {str(x["_id"]): x for x in users}

#     out = []
#     for oid in follower_ids:
#         uu = by_id.get(str(oid))
#         if uu:
#             out.append(_user_public(uu, viewer_id=str(g.user_id)))

#     return jsonify({"users": out}), 200


# # -------------------------
# # FOLLOWING LIST
# # -------------------------
# @user_bp.get("/<username>/following")
# @auth_required
# def following(username):
#     db = get_db()
#     u = db.users.find_one({"username": username})
#     if not u:
#         return jsonify({"error": "User not found"}), 404

#     limit = min(int(request.args.get("limit") or 20), 50)
#     skip = max(int(request.args.get("skip") or 0), 0)

#     user_oid = u["_id"]

#     cursor = db.follows.find({"follower_id": user_oid}).skip(skip).limit(limit)
#     following_ids = [x.get("following_id") for x in cursor if x.get("following_id")]

#     if not following_ids:
#         return jsonify({"users": []}), 200

#     users = list(db.users.find({"_id": {"$in": following_ids}}))
#     by_id = {str(x["_id"]): x for x in users}

#     out = []
#     for oid in following_ids:
#         uu = by_id.get(str(oid))
#         if uu:
#             out.append(_user_public(uu, viewer_id=str(g.user_id)))

#     return jsonify({"users": out}), 200


# # -------------------------
# # SUGGESTIONS
# # -------------------------
# @user_bp.get("/suggestions")
# @auth_required
# def suggestions():
#     db = get_db()
#     limit = min(int(request.args.get("limit") or 6), 20)

#     viewer_oid = _oid(g.user_id)
#     if not viewer_oid:
#         return jsonify({"error": "Invalid viewer id"}), 400

#     following_docs = list(db.follows.find({"follower_id": viewer_oid}, {"following_id": 1}))
#     following_set = {x["following_id"] for x in following_docs if x.get("following_id")}

#     exclude = set([viewer_oid]) | following_set

#     pipeline = [
#         {"$match": {"_id": {"$nin": list(exclude)}}},
#         {"$addFields": {"posts_count": {"$ifNull": ["$posts_count", 0]}}},
#         {"$sort": {"posts_count": -1, "followers_count": -1}},
#         {"$limit": max(limit * 3, 20)},
#     ]

#     candidates = list(db.users.aggregate(pipeline))
#     out = [_user_public(u, viewer_id=str(g.user_id)) for u in candidates[:limit]]

#     return jsonify({"users": out}), 200

# app/routes/user_routes.py
from datetime import datetime
from typing import Optional

from flask import Blueprint, jsonify, request, g
from bson import ObjectId

from app.middleware.auth_required import auth_required
from app.extensions import get_db

# ✅ IMPORTANT: This name MUST be user_bp
user_bp = Blueprint("users", __name__, url_prefix="/api/users")


# -------------------------
# helpers
# -------------------------
def _oid(v):
    try:
        return ObjectId(str(v))
    except Exception:
        return None


def _safe_int(v, default=0):
    try:
        return int(v)
    except Exception:
        return default


def _author_match(user_oid: ObjectId):
    """
    ✅ FIX: posts.author_id might be stored as STRING OR ObjectId
    """
    return {"$or": [{"author_id": str(user_oid)}, {"author_id": user_oid}]}


def _user_public(u: dict, viewer_id: Optional[str] = None) -> dict:
    uid = str(u.get("_id"))
    out = {
        "_id": uid,
        "username": u.get("username") or "",
        "name": u.get("name") or u.get("username") or "",
        "bio": u.get("bio") or "",
        "website": u.get("website") or "",
        "avatar_url": u.get("avatar_url") or u.get("avatarUrl") or None,
        "postsCount": _safe_int(u.get("posts_count") or u.get("postsCount") or 0),
        "followersCount": _safe_int(u.get("followers_count") or u.get("followersCount") or 0),
        "followingCount": _safe_int(u.get("following_count") or u.get("followingCount") or 0),
        "isFollowing": False,
    }

    if viewer_id:
        db = get_db()
        vid = _oid(viewer_id)
        tid = _oid(uid)
        if vid and tid:
            out["isFollowing"] = (
                db.follows.find_one({"follower_id": vid, "following_id": tid}) is not None
            )

    return out


def _sync_user_counts(db, user_oid: ObjectId):
    posts_count = db.posts.count_documents(_author_match(user_oid))
    followers_count = db.follows.count_documents({"following_id": user_oid})
    following_count = db.follows.count_documents({"follower_id": user_oid})

    db.users.update_one(
        {"_id": user_oid},
        {"$set": {
            "posts_count": posts_count,
            "followers_count": followers_count,
            "following_count": following_count,
            "updated_at": datetime.utcnow(),
        }},
    )

    return posts_count, followers_count, following_count


# -------------------------
# ME
# -------------------------
@user_bp.get("/me")
@auth_required
def me():
    db = get_db()
    uid = _oid(g.user_id)
    if not uid:
        return jsonify({"error": "Invalid user id"}), 400

    u = db.users.find_one({"_id": uid})
    if not u:
        return jsonify({"error": "User not found"}), 404

    pc, fc, fic = _sync_user_counts(db, uid)
    u["posts_count"], u["followers_count"], u["following_count"] = pc, fc, fic

    return jsonify({"user": _user_public(u, viewer_id=str(g.user_id))}), 200


# -------------------------
# PUBLIC PROFILE
# -------------------------
@user_bp.get("/<username>")
@auth_required
def profile(username):
    db = get_db()
    u = db.users.find_one({"username": username})
    if not u:
        return jsonify({"error": "User not found"}), 404

    user_oid = u["_id"]
    pc, fc, fic = _sync_user_counts(db, user_oid)
    u["posts_count"], u["followers_count"], u["following_count"] = pc, fc, fic

    return jsonify({"user": _user_public(u, viewer_id=str(g.user_id))}), 200


# -------------------------
# USER POSTS
# -------------------------
@user_bp.get("/<username>/posts")
@auth_required
def user_posts(username):
    db = get_db()
    u = db.users.find_one({"username": username})
    if not u:
        return jsonify({"error": "User not found"}), 404

    uid = u["_id"]
    cursor = db.posts.find(_author_match(uid)).sort("created_at", -1).limit(60)

    posts = []
    for p in cursor:
        posts.append({
            "_id": str(p["_id"]),
            "caption": p.get("caption") or "",
            "media_url": p.get("media_url") or p.get("mediaUrl"),
            "media_type": p.get("media_type") or p.get("mediaType"),
            "created_at": p.get("created_at").isoformat() if p.get("created_at") else None,
        })

    return jsonify({"posts": posts}), 200


# -------------------------
# FOLLOWERS LIST
# -------------------------
@user_bp.get("/<username>/followers")
@auth_required
def followers(username):
    db = get_db()
    u = db.users.find_one({"username": username})
    if not u:
        return jsonify({"error": "User not found"}), 404

    limit = min(int(request.args.get("limit") or 20), 50)
    skip = max(int(request.args.get("skip") or 0), 0)

    user_oid = u["_id"]
    rel = list(
        db.follows.find({"following_id": user_oid})
        .sort("created_at", -1)
        .skip(skip)
        .limit(limit)
    )

    follower_ids = [x.get("follower_id") for x in rel if x.get("follower_id")]
    if not follower_ids:
        return jsonify({"users": []}), 200

    users = list(db.users.find({"_id": {"$in": follower_ids}}))
    by_id = {str(x["_id"]): x for x in users}

    out = []
    for oid in follower_ids:
        uu = by_id.get(str(oid))
        if uu:
            out.append(_user_public(uu, viewer_id=str(g.user_id)))

    return jsonify({"users": out}), 200


# -------------------------
# FOLLOWING LIST
# -------------------------
@user_bp.get("/<username>/following")
@auth_required
def following(username):
    db = get_db()
    u = db.users.find_one({"username": username})
    if not u:
        return jsonify({"error": "User not found"}), 404

    limit = min(int(request.args.get("limit") or 20), 50)
    skip = max(int(request.args.get("skip") or 0), 0)

    user_oid = u["_id"]
    rel = list(
        db.follows.find({"follower_id": user_oid})
        .sort("created_at", -1)
        .skip(skip)
        .limit(limit)
    )

    following_ids = [x.get("following_id") for x in rel if x.get("following_id")]
    if not following_ids:
        return jsonify({"users": []}), 200

    users = list(db.users.find({"_id": {"$in": following_ids}}))
    by_id = {str(x["_id"]): x for x in users}

    out = []
    for oid in following_ids:
        uu = by_id.get(str(oid))
        if uu:
            out.append(_user_public(uu, viewer_id=str(g.user_id)))

    return jsonify({"users": out}), 200


# -------------------------
# SUGGESTIONS
# -------------------------
@user_bp.get("/suggestions")
@auth_required
def suggestions():
    db = get_db()
    limit = min(int(request.args.get("limit") or 6), 20)

    viewer_oid = _oid(g.user_id)
    if not viewer_oid:
        return jsonify({"error": "Invalid viewer id"}), 400

    following_docs = list(
        db.follows.find({"follower_id": viewer_oid}, {"following_id": 1})
    )
    following_set = {x["following_id"] for x in following_docs if x.get("following_id")}

    exclude = set([viewer_oid]) | following_set

    pipeline = [
        {"$match": {"_id": {"$nin": list(exclude)}}},
        {"$addFields": {"posts_count": {"$ifNull": ["$posts_count", 0]}}},
        {"$sort": {"posts_count": -1, "followers_count": -1}},
        {"$limit": max(limit * 3, 20)},
    ]

    candidates = list(db.users.aggregate(pipeline))
    out = [_user_public(u, viewer_id=str(g.user_id)) for u in candidates[:limit]]
    return jsonify({"users": out}), 200