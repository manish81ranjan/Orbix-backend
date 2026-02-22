# from flask import Blueprint, request, jsonify, g
# from app.middleware.auth_required import auth_required
# from app.utils.pagination import get_pagination_params

# from app.services.feed_service import get_home_feed
# from app.services.post_service import create_new_post, get_post

# post_bp = Blueprint("posts", __name__)


# @post_bp.route("/feed", methods=["GET"])
# @auth_required
# def feed():
#     page, limit, skip = get_pagination_params(request, default_limit=10)
#     posts = get_home_feed(page, limit, skip)
#     return jsonify({"posts": posts, "page": page, "limit": limit}), 200


# @post_bp.route("", methods=["POST"])
# @auth_required
# def create():
#     data = request.get_json(force=True) or {}
#     caption = data.get("caption", "")
#     media_url = data.get("mediaUrl") or data.get("media_url")  # support both

#     try:
#         post = create_new_post(g.current_user, caption, media_url)
#         return jsonify({"post": post}), 201
#     except ValueError as e:
#         return jsonify({"message": str(e)}), 400


# @post_bp.route("/<post_id>", methods=["GET"])
# @auth_required
# def get_one(post_id):
#     try:
#         post = get_post(post_id)
#         return jsonify({"post": post}), 200
#     except ValueError as e:
#         return jsonify({"message": str(e)}), 404
# from flask import Blueprint, request, jsonify, g
# from app.middleware.auth_required import auth_required
# from app.utils.pagination import get_pagination_params

# from app.services.feed_service import get_home_feed
# from app.services.post_service import create_new_post, get_post

# post_bp = Blueprint("posts", __name__)


# # Optional: preflight safety
# @post_bp.route("/feed", methods=["OPTIONS"])
# @post_bp.route("/", methods=["OPTIONS"])
# @post_bp.route("/<post_id>", methods=["OPTIONS"])
# def posts_options(post_id=None):
#     return ("", 204)


# @post_bp.route("/feed", methods=["GET"])
# @auth_required
# def feed():
#     page, limit, skip = get_pagination_params(request, default_limit=10)
#     posts = get_home_feed(page, limit, skip)
#     return jsonify({"posts": posts, "page": page, "limit": limit}), 200


# @post_bp.route("/", methods=["POST"])
# @auth_required
# def create():
#     if not getattr(g, "current_user", None):
#         return jsonify({"error": "Unauthorized"}), 401

#     data = request.get_json(silent=True) or {}
#     caption = (data.get("caption") or "").strip()
#     media_url = data.get("mediaUrl") or data.get("media_url")  # support both

#     try:
#         post = create_new_post(g.current_user, caption, media_url)
#         return jsonify({"post": post}), 201
#     except ValueError as e:
#         return jsonify({"error": str(e)}), 400


# @post_bp.route("/<post_id>", methods=["GET"])
# @auth_required
# def get_one(post_id):
#     try:
#         post = get_post(post_id)
#         return jsonify({"post": post}), 200
#     except ValueError as e:
#         return jsonify({"error": str(e)}), 404
# from flask import Blueprint, request, jsonify, g
# from app.middleware.auth_required import auth_required
# from app.models.post_model import create_post, serialize_post

# post_bp = Blueprint("posts", __name__)

# @post_bp.route("", methods=["POST"])
# @auth_required
# def create_post_route():
#     data = request.get_json(silent=True) or {}

#     caption = (data.get("caption") or "").strip()
#     media_url = (data.get("media_url") or data.get("mediaUrl") or "").strip()

#     if not caption and not media_url:
#         return jsonify({"message": "caption or media is required"}), 400

#     # You can decide media_type/is_reel later
#     post = create_post(
#         author_id=g.user_id,
#         author_username=g.get("username", "user"),  # optional if you set in token
#         caption=caption,
#         media_url=media_url or None
#     )

#     return jsonify({"post": serialize_post(post)}), 201


# @post_bp.route("/feed", methods=["GET"])
# @auth_required
# def feed():
#     # Return empty for now to avoid frontend crash
#     return jsonify({"posts": []}), 200
# from flask import Blueprint, request, jsonify, g
# from bson import ObjectId

# from app.middleware.auth_required import auth_required
# from app.models.post_model import create_post, serialize_post
# from app.extensions import get_db

# post_bp = Blueprint("posts", __name__)

# @post_bp.route("", methods=["POST", "OPTIONS"])
# @auth_required
# def create_post_route():
#     if request.method == "OPTIONS":
#         return ("", 204)

#     data = request.get_json(silent=True) or {}

#     caption = (data.get("caption") or "").strip()
#     media_url = (data.get("media_url") or data.get("mediaUrl") or "").strip()
#     media_type = (data.get("media_type") or "").strip()  # image | video

#     if not caption and not media_url:
#         return jsonify({"error": "caption or media is required"}), 400

#     post = create_post(
#     author_id=g.user_id,
#     author_username=getattr(g, "username", None) or "user",
#     caption=caption,
#     media_url=media_url or None,
#     media_type=media_type or None,
# )

#     return jsonify({"post": serialize_post(post)}), 201


# @post_bp.route("/feed", methods=["GET", "OPTIONS"])
# @auth_required
# def feed():
#     if request.method == "OPTIONS":
#         return ("", 204)

#     db = get_db()
#     posts = list(db.posts.find({}).sort("created_at", -1).limit(50))
#     return jsonify({"posts": [serialize_post(p) for p in posts]}), 200


# @post_bp.route("/<post_id>", methods=["GET", "OPTIONS"])
# @auth_required
# def get_post(post_id):
#     if request.method == "OPTIONS":
#         return ("", 204)

#     db = get_db()
#     try:
#         post = db.posts.find_one({"_id": ObjectId(post_id)})
#     except Exception:
#         post = None

#     if not post:
#         return jsonify({"error": "Post not found"}), 404

#     return jsonify({"post": serialize_post(post)}), 200


# from flask import Blueprint, request, jsonify, g
# from bson import ObjectId

# from app.middleware.auth_required import auth_required
# from app.extensions import get_db
# from app.models.post_model import create_post, serialize_post
# from app.models.comment_model import add_comment, list_comments, serialize_comment

# post_bp = Blueprint("posts", __name__, url_prefix="/api/posts")


# def _oid(x: str):
#     try:
#         return ObjectId(x)
#     except Exception:
#         return None


# def _add_flags(posts, user_id: str):
#     """
#     Adds likedByMe / savedByMe by checking likes+saves collections
#     """
#     db = get_db()
#     uid = _oid(user_id)
#     if not uid:
#         return [serialize_post(p) for p in posts]

#     post_ids = [p["_id"] for p in posts]

#     liked = set(
#         str(x["post_id"])
#         for x in db.likes.find({"user_id": uid, "post_id": {"$in": post_ids}}, {"post_id": 1})
#     )
#     saved = set(
#         str(x["post_id"])
#         for x in db.saves.find({"user_id": uid, "post_id": {"$in": post_ids}}, {"post_id": 1})
#     )

#     out = []
#     for p in posts:
#         sp = serialize_post(p)
#         pid = sp["_id"]
#         sp["likedByMe"] = pid in liked
#         sp["savedByMe"] = pid in saved
#         sp["liked_by_me"] = pid in liked
#         sp["saved_by_me"] = pid in saved
#         out.append(sp)
#     return out


# @post_bp.route("", methods=["POST", "OPTIONS"])
# @auth_required
# def create_post_route():
#     if request.method == "OPTIONS":
#         return ("", 204)

#     data = request.get_json(silent=True) or {}

#     caption = (data.get("caption") or "").strip()
#     media_url = (data.get("media_url") or data.get("mediaUrl") or "").strip()
#     media_type = (data.get("media_type") or data.get("mediaType") or "").strip()

#     if not caption and not media_url:
#         return jsonify({"error": "caption or media is required"}), 400

#     post = create_post(
#         author_id=g.user_id,
#         author_username=getattr(g, "username", None) or "user",
#         caption=caption,
#         media_url=media_url or None,
#         media_type=media_type or None,
#     )

#     return jsonify({"post": serialize_post(post)}), 201


# @post_bp.route("/feed", methods=["GET", "OPTIONS"])
# @auth_required
# def feed():
#     if request.method == "OPTIONS":
#         return ("", 204)

#     db = get_db()
#     posts = list(db.posts.find({}).sort("created_at", -1).limit(50))
#     return jsonify({"posts": _add_flags(posts, g.user_id)}), 200


# @post_bp.route("/<post_id>", methods=["GET", "OPTIONS"])
# @auth_required
# def get_post(post_id):
#     if request.method == "OPTIONS":
#         return ("", 204)

#     db = get_db()
#     pid = _oid(post_id)
#     if not pid:
#         return jsonify({"error": "Invalid post id"}), 400

#     post = db.posts.find_one({"_id": pid})
#     if not post:
#         return jsonify({"error": "Post not found"}), 404

#     return jsonify({"post": _add_flags([post], g.user_id)[0]}), 200


# # ---------- Likes ----------
# @post_bp.route("/<post_id>/like", methods=["POST", "OPTIONS"])
# @auth_required
# def like_post(post_id):
#     if request.method == "OPTIONS":
#         return ("", 204)

#     db = get_db()
#     pid = _oid(post_id)
#     uid = _oid(g.user_id)
#     if not pid or not uid:
#         return jsonify({"error": "Invalid ids"}), 400

#     existed = db.likes.find_one({"post_id": pid, "user_id": uid})
#     if existed:
#         return jsonify({"ok": True}), 200

#     db.likes.insert_one({"post_id": pid, "user_id": uid})
#     db.posts.update_one({"_id": pid}, {"$inc": {"likes_count": 1}})
#     return jsonify({"ok": True}), 200


# @post_bp.route("/<post_id>/unlike", methods=["POST", "OPTIONS"])
# @auth_required
# def unlike_post(post_id):
#     if request.method == "OPTIONS":
#         return ("", 204)

#     db = get_db()
#     pid = _oid(post_id)
#     uid = _oid(g.user_id)
#     if not pid or not uid:
#         return jsonify({"error": "Invalid ids"}), 400

#     deleted = db.likes.delete_one({"post_id": pid, "user_id": uid}).deleted_count
#     if deleted:
#         db.posts.update_one({"_id": pid}, {"$inc": {"likes_count": -1}})
#     return jsonify({"ok": True}), 200


# # ---------- Saves ----------
# @post_bp.route("/<post_id>/save", methods=["POST", "OPTIONS"])
# @auth_required
# def save_post(post_id):
#     if request.method == "OPTIONS":
#         return ("", 204)

#     db = get_db()
#     pid = _oid(post_id)
#     uid = _oid(g.user_id)
#     if not pid or not uid:
#         return jsonify({"error": "Invalid ids"}), 400

#     existed = db.saves.find_one({"post_id": pid, "user_id": uid})
#     if existed:
#         return jsonify({"ok": True}), 200

#     db.saves.insert_one({"post_id": pid, "user_id": uid})
#     db.posts.update_one({"_id": pid}, {"$inc": {"saves_count": 1}})
#     return jsonify({"ok": True}), 200


# @post_bp.route("/<post_id>/unsave", methods=["POST", "OPTIONS"])
# @auth_required
# def unsave_post(post_id):
#     if request.method == "OPTIONS":
#         return ("", 204)

#     db = get_db()
#     pid = _oid(post_id)
#     uid = _oid(g.user_id)
#     if not pid or not uid:
#         return jsonify({"error": "Invalid ids"}), 400

#     deleted = db.saves.delete_one({"post_id": pid, "user_id": uid}).deleted_count
#     if deleted:
#         db.posts.update_one({"_id": pid}, {"$inc": {"saves_count": -1}})
#     return jsonify({"ok": True}), 200


# # ---------- Comments ----------
# @post_bp.route("/<post_id>/comments", methods=["GET", "OPTIONS"])
# @auth_required
# def get_comments(post_id):
#     if request.method == "OPTIONS":
#         return ("", 204)

#     try:
#         comments = list_comments(post_id, limit=50)
#     except Exception:
#         return jsonify({"error": "Invalid post id"}), 400

#     return jsonify({"comments": [serialize_comment(c) for c in comments]}), 200


# @post_bp.route("/<post_id>/comments", methods=["POST", "OPTIONS"])
# @auth_required
# def create_comment(post_id):
#     if request.method == "OPTIONS":
#         return ("", 204)

#     data = request.get_json(silent=True) or {}
#     text = (data.get("text") or "").strip()
#     if not text:
#         return jsonify({"error": "Comment text required"}), 400

#     try:
#         c = add_comment(
#             post_id=post_id,
#             author_id=g.user_id,
#             author_username=getattr(g, "username", None) or "user",
#             text=text,
#         )
#     except Exception:
#         return jsonify({"error": "Invalid post id"}), 400

#     return jsonify({"comment": serialize_comment(c)}), 201

# from backend.app.models.comment_model import serialize_comment
# from flask import Blueprint, request, jsonify, g
# # from bson import ObjectId
# from datetime import datetime

# # from app.middleware.auth_required import auth_required
# # from app.extensions import get_db
# from app.models.post_model import create_post, serialize_post



# post_bp = Blueprint("posts", __name__, url_prefix="/api/posts")


# def _oid(v: str):
#     try:
#         return ObjectId(v)
#     except Exception:
#         return None


# # ---------- Create Post ----------
# @post_bp.route("", methods=["POST", "OPTIONS"])
# @auth_required
# def create_post_route():
#     if request.method == "OPTIONS":
#         return ("", 204)

#     data = request.get_json(silent=True) or {}
#     caption = (data.get("caption") or "").strip()
#     media_url = (data.get("media_url") or data.get("mediaUrl") or "").strip()
#     media_type = (data.get("media_type") or data.get("mediaType") or "").strip()

#     if not caption and not media_url:
#         return jsonify({"error": "caption or media is required"}), 400

#     post = create_post(
#         author_id=g.user_id,
#         author_username=getattr(g, "username", None) or "user",
#         caption=caption,
#         media_url=media_url or None,
#         media_type=media_type or None,
#     )

#     return jsonify({"post": serialize_post(post, user_id=g.user_id)}), 201


# # ---------- Feed ----------
# @post_bp.route("/feed", methods=["GET", "OPTIONS"])
# @auth_required
# def feed():
#     if request.method == "OPTIONS":
#         return ("", 204)

#     db = get_db()
#     posts = list(db.posts.find({}).sort("created_at", -1).limit(50))
#     return jsonify({"posts": [serialize_post(p, user_id=g.user_id) for p in posts]}), 200


# # ---------- Get Single Post ----------
# @post_bp.route("/<post_id>", methods=["GET", "OPTIONS"])
# @auth_required
# def get_post(post_id):
#     if request.method == "OPTIONS":
#         return ("", 204)

#     db = get_db()
#     po = _oid(post_id)
#     if not po:
#         return jsonify({"error": "Invalid post id"}), 400

#     post = db.posts.find_one({"_id": po})
#     if not post:
#         return jsonify({"error": "Post not found"}), 404

#     return jsonify({"post": serialize_post(post, user_id=g.user_id)}), 200


# # ---------- Likes (persistent + idempotent) ----------
# @post_bp.route("/<post_id>/like", methods=["POST", "OPTIONS"])
# @auth_required
# def like_post(post_id):
#     if request.method == "OPTIONS":
#         return ("", 204)

#     db = get_db()
#     po = _oid(post_id)
#     uo = _oid(g.user_id)
#     if not po or not uo:
#         return jsonify({"error": "Invalid ids"}), 400

#     exists = db.likes.find_one({"post_id": po, "user_id": uo})
#     if exists:
#         return jsonify({"ok": True}), 200  # already liked

#     db.likes.insert_one({"post_id": po, "user_id": uo, "created_at": datetime.utcnow()})
#     db.posts.update_one({"_id": po}, {"$inc": {"likes_count": 1}})
#     return jsonify({"ok": True}), 200


# @post_bp.route("/<post_id>/unlike", methods=["POST", "OPTIONS"])
# @auth_required
# def unlike_post(post_id):
#     if request.method == "OPTIONS":
#         return ("", 204)

#     db = get_db()
#     po = _oid(post_id)
#     uo = _oid(g.user_id)
#     if not po or not uo:
#         return jsonify({"error": "Invalid ids"}), 400

#     deleted = db.likes.delete_one({"post_id": po, "user_id": uo}).deleted_count
#     if deleted:
#         db.posts.update_one({"_id": po}, {"$inc": {"likes_count": -1}})
#     return jsonify({"ok": True}), 200


# # ---------- Saves (persistent + idempotent) ----------
# @post_bp.route("/<post_id>/save", methods=["POST", "OPTIONS"])
# @auth_required
# def save_post(post_id):
#     if request.method == "OPTIONS":
#         return ("", 204)

#     db = get_db()
#     po = _oid(post_id)
#     uo = _oid(g.user_id)
#     if not po or not uo:
#         return jsonify({"error": "Invalid ids"}), 400

#     exists = db.saves.find_one({"post_id": po, "user_id": uo})
#     if exists:
#         return jsonify({"ok": True}), 200

#     db.saves.insert_one({"post_id": po, "user_id": uo, "created_at": datetime.utcnow()})
#     db.posts.update_one({"_id": po}, {"$inc": {"saves_count": 1}})
#     return jsonify({"ok": True}), 200


# @post_bp.route("/<post_id>/unsave", methods=["POST", "OPTIONS"])
# @auth_required
# def unsave_post(post_id):
#     if request.method == "OPTIONS":
#         return ("", 204)

#     db = get_db()
#     po = _oid(post_id)
#     uo = _oid(g.user_id)
#     if not po or not uo:
#         return jsonify({"error": "Invalid ids"}), 400

#     deleted = db.saves.delete_one({"post_id": po, "user_id": uo}).deleted_count
#     if deleted:
#         db.posts.update_one({"_id": po}, {"$inc": {"saves_count": -1}})
#     return jsonify({"ok": True}), 200


# # ---------- Comments (persistent) ----------
# @post_bp.route("/<post_id>/comments", methods=["GET", "OPTIONS"])
# @auth_required
# def list_comments(post_id):
#     if request.method == "OPTIONS":
#         return ("", 204)

#     db = get_db()
#     po = _oid(post_id)
#     if not po:
#         return jsonify({"error": "Invalid post id"}), 400

#     items = list(db.comments.find({"post_id": po}).sort("created_at", 1).limit(100))
#     out = []
#     for c in items:
#         created = c.get("created_at")
#         out.append({
#             "_id": str(c["_id"]),
#             "post_id": str(c.get("post_id")),
#             "author_id": str(c.get("author_id")) if c.get("author_id") else None,
#             "author_username": c.get("author_username", "unknown"),
#             "text": c.get("text", ""),
#             "created_at": created.isoformat() if created else None,

#             "postId": str(c.get("post_id")),
#             "authorUsername": c.get("author_username", "unknown"),
#             "createdAt": created.isoformat() if created else None,
#         })

#     return jsonify({"comments": out}), 200


# @post_bp.route("/<post_id>/comments", methods=["POST", "OPTIONS"])
# @auth_required
# def add_comment(post_id):
#     if request.method == "OPTIONS":
#         return ("", 204)

#     data = request.get_json(silent=True) or {}
#     text = (data.get("text") or "").strip()
#     if not text:
#         return jsonify({"error": "Comment text required"}), 400

#     db = get_db()
#     po = _oid(post_id)
#     uo = _oid(g.user_id)
#     if not po or not uo:
#         return jsonify({"error": "Invalid ids"}), 400

#     doc = {
#         "post_id": po,
#         "author_id": uo,
#         "author_username": getattr(g, "username", None) or "user",
#         "text": text,
#         "created_at": datetime.utcnow(),
#     }
#     res = db.comments.insert_one(doc)
#     doc["_id"] = res.inserted_id

#     db.posts.update_one({"_id": po}, {"$inc": {"comments_count": 1}})

#     created = doc.get("created_at")
#     return jsonify({
#         "comment": {
#             "_id": str(doc["_id"]),
#             "post_id": str(doc["post_id"]),
#             "author_id": str(doc["author_id"]),
#             "author_username": doc["author_username"],
#             "text": doc["text"],
#             "created_at": created.isoformat() if created else None,

#             "postId": str(doc["post_id"]),
#             "authorUsername": doc["author_username"],
#             "createdAt": created.isoformat() if created else None,
#         }
#     }), 201

# @post_bp.route("/<post_id>", methods=["DELETE", "OPTIONS"])
# @auth_required
# def delete_post(post_id):
#     if request.method == "OPTIONS":
#         return ("", 204)

#     db = get_db()
#     po = _oid(post_id)
#     if not po:
#         return jsonify({"error": "Invalid post id"}), 400

#     post = db.posts.find_one({"_id": po})
#     if not post:
#         return jsonify({"error": "Post not found"}), 404

#     # only owner can delete
#     if str(post.get("author_username")) != str(getattr(g, "username", "")):
#         return jsonify({"error": "Not allowed"}), 403

#     db.posts.delete_one({"_id": po})
#     db.comments.delete_many({"post_id": po})
#     db.likes.delete_many({"post_id": po})
#     db.saves.delete_many({"post_id": po})

#     return jsonify({"ok": True}), 200

# from bson import ObjectId
# # from flask import request, jsonify, g
# from app.middleware.auth_required import auth_required
# from app.extensions import get_db

# def _oid(x: str):
#     try:
#         return ObjectId(x)
#     except Exception:
#         return None

# @post_bp.route("/<post_id>", methods=["DELETE", "OPTIONS"])
# @auth_required
# def delete_post(post_id):
#     if request.method == "OPTIONS":
#         return ("", 204)

#     db = get_db()
#     po = _oid(post_id)
#     if not po:
#         return jsonify({"error": "Invalid post id"}), 400

#     post = db.posts.find_one({"_id": po})
#     if not post:
#         return jsonify({"error": "Post not found"}), 404

#     # owner check
#     if str(post.get("author_username")) != str(getattr(g, "username", "")):
#         return jsonify({"error": "Not allowed"}), 403

#     db.posts.delete_one({"_id": po})
#     db.comments.delete_many({"post_id": po})
#     db.likes.delete_many({"post_id": po})
#     db.saves.delete_many({"post_id": po})

#     return jsonify({"ok": True}), 200


#     post_bp = Blueprint("posts", __name__, url_prefix="/api/posts")


# @post_bp.route("", methods=["POST"])
# @auth_required
# def create_post_route():
#     data = request.get_json(silent=True) or {}

#     caption = (data.get("caption") or "").strip()
#     media_url = (data.get("media_url") or data.get("mediaUrl") or "").strip()
#     media_type = (data.get("media_type") or data.get("mediaType") or "").strip()

#     if not caption and not media_url:
#         return jsonify({"error": "caption or media is required"}), 400

#     post = create_post(
#         author_id=g.user_id,
#         author_username=getattr(g, "username", None) or "user",
#         caption=caption,
#         media_url=media_url or None,
#         media_type=media_type or None,
#     )

#     return jsonify({"post": serialize_post(post)}), 201


# @post_bp.route("/feed", methods=["GET"])
# @auth_required
# def feed():
#     db = get_db()
#     posts = list(db.posts.find({}).sort("created_at", -1).limit(50))
#     return jsonify({"posts": [serialize_post(p) for p in posts]}), 200


# @post_bp.route("/<post_id>", methods=["GET"])
# @auth_required
# def get_post(post_id):
#     db = get_db()
#     try:
#         post = db.posts.find_one({"_id": ObjectId(post_id)})
#     except Exception:
#         post = None

#     if not post:
#         return jsonify({"error": "Post not found"}), 404

#     return jsonify({"post": serialize_post(post)}), 200


# # ✅ ✅ ✅ DELETE POST (FIX)
# @post_bp.route("/<post_id>", methods=["DELETE"])
# @auth_required
# def delete_post(post_id):
#     db = get_db()

#     try:
#         pid = ObjectId(post_id)
#     except Exception:
#         return jsonify({"error": "Invalid post id"}), 400

#     post = db.posts.find_one({"_id": pid})
#     if not post:
#         return jsonify({"error": "Post not found"}), 404

#     # only author can delete
#     if str(post.get("author_id")) != str(g.user_id):
#         return jsonify({"error": "Not allowed"}), 403

#     # cleanup: comments, likes, saves
#     db.comments.delete_many({"post_id": pid})
#     db.likes.delete_many({"post_id": pid})
#     db.saves.delete_many({"post_id": pid})

#     # delete post
#     db.posts.delete_one({"_id": pid})

#     return jsonify({"ok": True}), 200


# # ---------- Likes ----------
# @post_bp.route("/<post_id>/like", methods=["POST"])
# @auth_required
# def like_post(post_id):
#     db = get_db()
#     uid = ObjectId(str(g.user_id))

#     try:
#         pid = ObjectId(post_id)
#     except Exception:
#         return jsonify({"error": "Invalid post id"}), 400

#     already = db.likes.find_one({"post_id": pid, "user_id": uid})
#     if already:
#         return jsonify({"ok": True}), 200

#     db.likes.insert_one({"post_id": pid, "user_id": uid})
#     db.posts.update_one({"_id": pid}, {"$inc": {"likes_count": 1}})
#     return jsonify({"ok": True}), 200


# @post_bp.route("/<post_id>/unlike", methods=["POST"])
# @auth_required
# def unlike_post(post_id):
#     db = get_db()
#     uid = ObjectId(str(g.user_id))

#     try:
#         pid = ObjectId(post_id)
#     except Exception:
#         return jsonify({"error": "Invalid post id"}), 400

#     deleted = db.likes.delete_one({"post_id": pid, "user_id": uid}).deleted_count
#     if deleted:
#         db.posts.update_one({"_id": pid}, {"$inc": {"likes_count": -1}})
#     return jsonify({"ok": True}), 200


# # ---------- Saves ----------
# @post_bp.route("/<post_id>/save", methods=["POST"])
# @auth_required
# def save_post(post_id):
#     db = get_db()
#     uid = ObjectId(str(g.user_id))

#     try:
#         pid = ObjectId(post_id)
#     except Exception:
#         return jsonify({"error": "Invalid post id"}), 400

#     already = db.saves.find_one({"post_id": pid, "user_id": uid})
#     if already:
#         return jsonify({"ok": True}), 200

#     db.saves.insert_one({"post_id": pid, "user_id": uid})
#     db.posts.update_one({"_id": pid}, {"$inc": {"saves_count": 1}})
#     return jsonify({"ok": True}), 200


# @post_bp.route("/<post_id>/unsave", methods=["POST"])
# @auth_required
# def unsave_post(post_id):
#     db = get_db()
#     uid = ObjectId(str(g.user_id))

#     try:
#         pid = ObjectId(post_id)
#     except Exception:
#         return jsonify({"error": "Invalid post id"}), 400

#     deleted = db.saves.delete_one({"post_id": pid, "user_id": uid}).deleted_count
#     if deleted:
#         db.posts.update_one({"_id": pid}, {"$inc": {"saves_count": -1}})
#     return jsonify({"ok": True}), 200


# # ---------- Comments ----------
# @post_bp.route("/<post_id>/comments", methods=["GET"])
# @auth_required
# def get_comments(post_id):
#     comments = list_comments(post_id)
#     return jsonify({"comments": [serialize_comment(c) for c in comments]}), 200


# @post_bp.route("/<post_id>/comments", methods=["POST"])
# @auth_required
# def create_comment(post_id):
#     data = request.get_json(silent=True) or {}
#     text = (data.get("text") or "").strip()
#     if not text:
#         return jsonify({"error": "Comment text required"}), 400

#     c = add_comment(
#         post_id=post_id,
#         author_id=str(g.user_id),
#         author_username=getattr(g, "username", None) or "user",
#         text=text,
#     )
#     return jsonify({"comment": serialize_comment(c)}), 201


#     @post_bp.route("/explore", methods=["GET"])
#     @auth_required
#     def explore():
#         """
#     REAL Explore:
#     - If q provided: search caption + author_username (case-insensitive)
#     - Else: returns latest posts (same as feed, but can be tuned later)
#     """
#     db = get_db()
#     q = (request.args.get("q") or "").strip()

#     query = {}
#     if q:
#         query = {
#             "$or": [
#                 {"caption": {"$regex": q, "$options": "i"}},
#                 {"author_username": {"$regex": q, "$options": "i"}},
#             ]
#         }

#     posts = list(db.posts.find(query).sort("created_at", -1).limit(60))
#     return jsonify({"posts": [serialize_post(p) for p in posts]}), 200

# from datetime import datetime
# from flask import Blueprint, request, jsonify, g
# from bson import ObjectId

# from app.middleware.auth_required import auth_required
# from app.extensions import get_db

# from app.models.post_model import create_post, serialize_post
# from app.models.comment_model import serialize_comment
# from app.models.notification_model import create_notification

# post_bp = Blueprint("posts", __name__, url_prefix="/api/posts")


# def _oid(v: str):
#     try:
#         return ObjectId(str(v))
#     except Exception:
#         return None


# # -------------------- CREATE POST --------------------
# @post_bp.route("", methods=["POST"])
# @auth_required
# def create_post_route():
#     data = request.get_json(silent=True) or {}

#     caption = (data.get("caption") or "").strip()
#     media_url = (data.get("media_url") or data.get("mediaUrl") or "").strip()
#     media_type = (data.get("media_type") or data.get("mediaType") or "").strip()

#     if not caption and not media_url:
#         return jsonify({"error": "caption or media is required"}), 400

#     post = create_post(
#         author_id=str(g.user_id),
#         author_username=getattr(g, "username", None) or "user",
#         caption=caption,
#         media_url=media_url or None,
#         media_type=media_type or None,
#     )

#     return jsonify({"post": serialize_post(post, user_id=str(g.user_id))}), 201


# # -------------------- FEED --------------------
# @post_bp.route("/feed", methods=["GET"])
# @auth_required
# def feed():
#     db = get_db()
#     posts = list(db.posts.find({}).sort("created_at", -1).limit(50))
#     return jsonify({"posts": [serialize_post(p, user_id=str(g.user_id)) for p in posts]}), 200


# # -------------------- EXPLORE (REAL) --------------------
# @post_bp.route("/explore", methods=["GET"])
# @auth_required
# def explore():
#     """
#     REAL explore:
#     - /api/posts/explore?q=manish  -> searches caption + username
#     - /api/posts/explore          -> latest posts
#     """
#     db = get_db()
#     q = (request.args.get("q") or "").strip()

#     query = {}
#     if q:
#         query = {
#             "$or": [
#                 {"caption": {"$regex": q, "$options": "i"}},
#                 {"author_username": {"$regex": q, "$options": "i"}},
#             ]
#         }

#     posts = list(db.posts.find(query).sort("created_at", -1).limit(60))
#     return jsonify({"posts": [serialize_post(p, user_id=str(g.user_id)) for p in posts]}), 200


# # -------------------- GET POST --------------------
# @post_bp.route("/<post_id>", methods=["GET"])
# @auth_required
# def get_post(post_id):
#     db = get_db()
#     pid = _oid(post_id)
#     if not pid:
#         return jsonify({"error": "Invalid post id"}), 400

#     post = db.posts.find_one({"_id": pid})
#     if not post:
#         return jsonify({"error": "Post not found"}), 404

#     return jsonify({"post": serialize_post(post, user_id=str(g.user_id))}), 200


# # -------------------- DELETE POST (FIXED) --------------------
# @post_bp.route("/<post_id>", methods=["DELETE"])
# @auth_required
# def delete_post(post_id):
#     db = get_db()
#     pid = _oid(post_id)
#     if not pid:
#         return jsonify({"error": "Invalid post id"}), 400

#     post = db.posts.find_one({"_id": pid})
#     if not post:
#         return jsonify({"error": "Post not found"}), 404

#     # ✅ correct owner check (by author_id)
#     if str(post.get("author_id")) != str(g.user_id):
#         return jsonify({"error": "Not allowed"}), 403

#     # cleanup
#     db.comments.delete_many({"post_id": pid})
#     db.likes.delete_many({"post_id": pid})
#     db.saves.delete_many({"post_id": pid})

#     db.posts.delete_one({"_id": pid})
#     return jsonify({"ok": True}), 200


# # -------------------- LIKE (idempotent) --------------------
# # @post_bp.route("/<post_id>/like", methods=["POST"])
# # @auth_required
# # def like_post(post_id):
# #     db = get_db()
# #     pid = _oid(post_id)
# #     uid = _oid(g.user_id)
# #     if not pid or not uid:
# #         return jsonify({"error": "Invalid ids"}), 400

# #     exists = db.likes.find_one({"post_id": pid, "user_id": uid})
# #     if exists:
# #         return jsonify({"ok": True}), 200

# #     db.likes.insert_one({"post_id": pid, "user_id": uid, "created_at": datetime.utcnow()})
# #     db.posts.update_one({"_id": pid}, {"$inc": {"likes_count": 1}})
# #     return jsonify({"ok": True}), 200

# @post_bp.route("/<post_id>/like", methods=["POST"])
# @auth_required
# def like_post(post_id):
#     db = get_db()
#     pid = _oid(post_id)
#     uid = _oid(g.user_id)

#     if not pid or not uid:
#         return jsonify({"error": "Invalid ids"}), 400

#     exists = db.likes.find_one({"post_id": pid, "user_id": uid})
#     if exists:
#         return jsonify({"ok": True}), 200

#     db.likes.insert_one({
#         "post_id": pid,
#         "user_id": uid,
#         "created_at": datetime.utcnow()
#     })

#     db.posts.update_one({"_id": pid}, {"$inc": {"likes_count": 1}})

#     # 🔥 CREATE NOTIFICATION
#     post = db.posts.find_one({"_id": pid})
#     if post and str(post.get("author_id")) != str(g.user_id):
#         create_notification(
#             user_id=str(post.get("author_id")),
#             from_user_id=str(g.user_id),
#             from_username=getattr(g, "username", None),
#             notif_type="like",
#             message="liked your post"
#         )

#     return jsonify({"ok": True}), 200
# @post_bp.route("/<post_id>/unlike", methods=["POST"])
# @auth_required
# def unlike_post(post_id):
#     db = get_db()
#     pid = _oid(post_id)
#     uid = _oid(g.user_id)
#     if not pid or not uid:
#         return jsonify({"error": "Invalid ids"}), 400

#     deleted = db.likes.delete_one({"post_id": pid, "user_id": uid}).deleted_count
#     if deleted:
#         db.posts.update_one({"_id": pid}, {"$inc": {"likes_count": -1}})
#     return jsonify({"ok": True}), 200


# # -------------------- SAVE (idempotent) --------------------
# @post_bp.route("/<post_id>/save", methods=["POST"])
# @auth_required
# def save_post(post_id):
#     db = get_db()
#     pid = _oid(post_id)
#     uid = _oid(g.user_id)
#     if not pid or not uid:
#         return jsonify({"error": "Invalid ids"}), 400

#     exists = db.saves.find_one({"post_id": pid, "user_id": uid})
#     if exists:
#         return jsonify({"ok": True}), 200

#     db.saves.insert_one({"post_id": pid, "user_id": uid, "created_at": datetime.utcnow()})
#     db.posts.update_one({"_id": pid}, {"$inc": {"saves_count": 1}})
#     return jsonify({"ok": True}), 200


# @post_bp.route("/<post_id>/unsave", methods=["POST"])
# @auth_required
# def unsave_post(post_id):
#     db = get_db()
#     pid = _oid(post_id)
#     uid = _oid(g.user_id)
#     if not pid or not uid:
#         return jsonify({"error": "Invalid ids"}), 400

#     deleted = db.saves.delete_one({"post_id": pid, "user_id": uid}).deleted_count
#     if deleted:
#         db.posts.update_one({"_id": pid}, {"$inc": {"saves_count": -1}})
#     return jsonify({"ok": True}), 200


# # -------------------- COMMENTS --------------------
# @post_bp.route("/<post_id>/comments", methods=["POST"])
# @auth_required
# def add_comment(post_id):
#     data = request.get_json(silent=True) or {}
#     text = (data.get("text") or "").strip()
#     if not text:
#         return jsonify({"error": "Comment text required"}), 400

#     db = get_db()
#     pid = _oid(post_id)
#     uid = _oid(g.user_id)

#     if not pid or not uid:
#         return jsonify({"error": "Invalid ids"}), 400

#     doc = {
#         "post_id": pid,
#         "author_id": uid,
#         "author_username": getattr(g, "username", None) or "user",
#         "text": text,
#         "created_at": datetime.utcnow(),
#     }

#     res = db.comments.insert_one(doc)
#     doc["_id"] = res.inserted_id

#     db.posts.update_one({"_id": pid}, {"$inc": {"comments_count": 1}})

#     # 🔥 CREATE NOTIFICATION
#     post = db.posts.find_one({"_id": pid})
#     if post and str(post.get("author_id")) != str(g.user_id):
#         create_notification(
#             user_id=str(post.get("author_id")),
#             from_user_id=str(g.user_id),
#             from_username=getattr(g, "username", None),
#             notif_type="comment",
#             message=f'commented: "{text[:50]}"'
#         )

#     return jsonify({"comment": serialize_comment(doc)}), 201

# # @post_bp.route("/<post_id>/comments", methods=["POST"])
# # @auth_required
# # def add_comment(post_id):
# #     data = request.get_json(silent=True) or {}
# #     text = (data.get("text") or "").strip()
# #     if not text:
# #         return jsonify({"error": "Comment text required"}), 400

# #     db = get_db()
# #     pid = _oid(post_id)
# #     uid = _oid(g.user_id)
# #     if not pid or not uid:
# #         return jsonify({"error": "Invalid ids"}), 400

# #     doc = {
# #         "post_id": pid,
# #         "author_id": uid,
# #         "author_username": getattr(g, "username", None) or "user",
# #         "text": text,
# #         "created_at": datetime.utcnow(),
# #     }
# #     res = db.comments.insert_one(doc)
# #     doc["_id"] = res.inserted_id

# #     db.posts.update_one({"_id": pid}, {"$inc": {"comments_count": 1}})

# #     return jsonify({"comment": serialize_comment(doc)}), 201

from datetime import datetime
from flask import Blueprint, request, jsonify, g
from bson import ObjectId

from app.middleware.auth_required import auth_required
from app.extensions import get_db

from app.models.post_model import create_post, serialize_post
from app.models.comment_model import serialize_comment
from app.models.notification_model import create_notification

post_bp = Blueprint("posts", __name__, url_prefix="/api/posts")


def _oid(v: str):
    try:
        return ObjectId(str(v))
    except Exception:
        return None


# -------------------- CREATE POST --------------------
@post_bp.route("", methods=["POST"])
@auth_required
def create_post_route():
    data = request.get_json(silent=True) or {}

    caption = (data.get("caption") or "").strip()
    media_url = (data.get("media_url") or data.get("mediaUrl") or "").strip()
    media_type = (data.get("media_type") or data.get("mediaType") or "").strip()

    if not caption and not media_url:
        return jsonify({"error": "caption or media is required"}), 400

    post = create_post(
        author_id=str(g.user_id),
        author_username=getattr(g, "username", None) or "user",
        caption=caption,
        media_url=media_url or None,
        media_type=media_type or None,
    )

    return jsonify({"post": serialize_post(post, user_id=str(g.user_id))}), 201


# -------------------- FEED --------------------
@post_bp.route("/feed", methods=["GET"])
@auth_required
def feed():
    db = get_db()
    posts = list(db.posts.find({}).sort("created_at", -1).limit(50))
    return jsonify({"posts": [serialize_post(p, user_id=str(g.user_id)) for p in posts]}), 200


# -------------------- EXPLORE --------------------
@post_bp.route("/explore", methods=["GET"])
@auth_required
def explore():
    db = get_db()
    q = (request.args.get("q") or "").strip()

    query = {}
    if q:
        query = {
            "$or": [
                {"caption": {"$regex": q, "$options": "i"}},
                {"author_username": {"$regex": q, "$options": "i"}},
            ]
        }

    posts = list(db.posts.find(query).sort("created_at", -1).limit(60))
    return jsonify({"posts": [serialize_post(p, user_id=str(g.user_id)) for p in posts]}), 200


# -------------------- GET SINGLE POST --------------------
@post_bp.route("/<post_id>", methods=["GET"])
@auth_required
def get_post(post_id):
    db = get_db()
    pid = _oid(post_id)
    if not pid:
        return jsonify({"error": "Invalid post id"}), 400

    post = db.posts.find_one({"_id": pid})
    if not post:
        return jsonify({"error": "Post not found"}), 404

    return jsonify({"post": serialize_post(post, user_id=str(g.user_id))}), 200


# -------------------- DELETE POST --------------------
@post_bp.route("/<post_id>", methods=["DELETE"])
@auth_required
def delete_post(post_id):
    db = get_db()
    pid = _oid(post_id)
    if not pid:
        return jsonify({"error": "Invalid post id"}), 400

    post = db.posts.find_one({"_id": pid})
    if not post:
        return jsonify({"error": "Post not found"}), 404

    # ✅ only author can delete (use author_id, not username)
    if str(post.get("author_id")) != str(g.user_id):
        return jsonify({"error": "Not allowed"}), 403

    db.comments.delete_many({"post_id": pid})
    db.likes.delete_many({"post_id": pid})
    db.saves.delete_many({"post_id": pid})
    db.posts.delete_one({"_id": pid})

    return jsonify({"ok": True}), 200


# -------------------- LIKE --------------------
@post_bp.route("/<post_id>/like", methods=["POST"])
@auth_required
def like_post(post_id):
    db = get_db()
    pid = _oid(post_id)
    uid = _oid(g.user_id)

    if not pid or not uid:
        return jsonify({"error": "Invalid ids"}), 400

    exists = db.likes.find_one({"post_id": pid, "user_id": uid})
    if exists:
        return jsonify({"ok": True}), 200

    db.likes.insert_one({"post_id": pid, "user_id": uid, "created_at": datetime.utcnow()})
    db.posts.update_one({"_id": pid}, {"$inc": {"likes_count": 1}})

    # 🔔 notify author (skip self-like)
    post = db.posts.find_one({"_id": pid})
    if post and str(post.get("author_id")) != str(g.user_id):
        create_notification(
            user_id=str(post.get("author_id")),
            from_user_id=str(g.user_id),
            from_username=getattr(g, "username", None),
            notif_type="like",
            message="liked your post",
        )

    return jsonify({"ok": True}), 200


@post_bp.route("/<post_id>/unlike", methods=["POST"])
@auth_required
def unlike_post(post_id):
    db = get_db()
    pid = _oid(post_id)
    uid = _oid(g.user_id)

    if not pid or not uid:
        return jsonify({"error": "Invalid ids"}), 400

    deleted = db.likes.delete_one({"post_id": pid, "user_id": uid}).deleted_count
    if deleted:
        db.posts.update_one({"_id": pid}, {"$inc": {"likes_count": -1}})

    return jsonify({"ok": True}), 200


# -------------------- SAVE --------------------
@post_bp.route("/<post_id>/save", methods=["POST"])
@auth_required
def save_post(post_id):
    db = get_db()
    pid = _oid(post_id)
    uid = _oid(g.user_id)

    if not pid or not uid:
        return jsonify({"error": "Invalid ids"}), 400

    exists = db.saves.find_one({"post_id": pid, "user_id": uid})
    if exists:
        return jsonify({"ok": True}), 200

    db.saves.insert_one({"post_id": pid, "user_id": uid, "created_at": datetime.utcnow()})
    db.posts.update_one({"_id": pid}, {"$inc": {"saves_count": 1}})

    return jsonify({"ok": True}), 200


@post_bp.route("/<post_id>/unsave", methods=["POST"])
@auth_required
def unsave_post(post_id):
    db = get_db()
    pid = _oid(post_id)
    uid = _oid(g.user_id)

    if not pid or not uid:
        return jsonify({"error": "Invalid ids"}), 400

    deleted = db.saves.delete_one({"post_id": pid, "user_id": uid}).deleted_count
    if deleted:
        db.posts.update_one({"_id": pid}, {"$inc": {"saves_count": -1}})

    return jsonify({"ok": True}), 200


# -------------------- COMMENTS (GET ✅) --------------------
@post_bp.route("/<post_id>/comments", methods=["GET"])
@auth_required
def get_comments(post_id):
    db = get_db()
    pid = _oid(post_id)
    if not pid:
        return jsonify({"error": "Invalid post id"}), 400

    items = list(db.comments.find({"post_id": pid}).sort("created_at", 1).limit(100))
    return jsonify({"comments": [serialize_comment(c) for c in items]}), 200


# -------------------- COMMENTS (POST ✅) --------------------
@post_bp.route("/<post_id>/comments", methods=["POST"])
@auth_required
def add_comment(post_id):
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    if not text:
        return jsonify({"error": "Comment text required"}), 400

    db = get_db()
    pid = _oid(post_id)
    uid = _oid(g.user_id)
    if not pid or not uid:
        return jsonify({"error": "Invalid ids"}), 400

    doc = {
        "post_id": pid,
        "author_id": uid,
        "author_username": getattr(g, "username", None) or "user",
        "text": text,
        "created_at": datetime.utcnow(),
    }
    res = db.comments.insert_one(doc)
    doc["_id"] = res.inserted_id

    db.posts.update_one({"_id": pid}, {"$inc": {"comments_count": 1}})

    # 🔔 notify author (skip self-comment)
    post = db.posts.find_one({"_id": pid})
    if post and str(post.get("author_id")) != str(g.user_id):
        create_notification(
            user_id=str(post.get("author_id")),
            from_user_id=str(g.user_id),
            from_username=getattr(g, "username", None),
            notif_type="comment",
            message=f'commented: "{text[:50]}"',
        )

    return jsonify({"comment": serialize_comment(doc)}), 201