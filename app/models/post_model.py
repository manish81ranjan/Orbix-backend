# from datetime import datetime
# from bson import ObjectId
# from app.extensions import get_db


# def _oid(value: str):
#     try:
#         return ObjectId(value)
#     except Exception:
#         return None


# def serialize_post(post: dict) -> dict:
#     created = post.get("created_at")
#     return {
#         "_id": str(post["_id"]),
#         "author_id": str(post.get("author_id")) if post.get("author_id") else None,
#         "author_username": post.get("author_username"),
#         "caption": post.get("caption", ""),
#         "media_url": post.get("media_url"),
#         "likes_count": post.get("likes_count", 0),
#         "comments_count": post.get("comments_count", 0),
#         "created_at": created.isoformat() if created else None
#     }


# def create_post(author_id: str, author_username: str, caption: str, media_url: str | None):
#     author_oid = _oid(author_id)
#     if not author_oid:
#         raise ValueError("Invalid author_id")

#     db = get_db()
#     doc = {
#         "author_id": author_oid,
#         "author_username": author_username,
#         "caption": caption or "",
#         "media_url": media_url or None,
#         "likes_count": 0,
#         "comments_count": 0,
#         "created_at": datetime.utcnow()
#     }
#     res = db.posts.insert_one(doc)
#     doc["_id"] = res.inserted_id
#     return doc


# def get_post_by_id(post_id: str):
#     post_oid = _oid(post_id)
#     if not post_oid:
#         return None
#     db = get_db()
#     return db.posts.find_one({"_id": post_oid})


# def get_feed(page: int, limit: int, skip: int):
#     db = get_db()
#     cursor = db.posts.find({}).sort("created_at", -1).skip(skip).limit(limit)
#     return list(cursor)
# backend/app/models/post_model.py

# from datetime import datetime
# from bson import ObjectId
# from app.extensions import get_db

# def serialize_post(post: dict) -> dict:
#     created = post.get("created_at")
#     created_iso = created.isoformat() if created else None

#     out = {
#         "_id": str(post["_id"]),
#         "author_id": str(post.get("author_id")) if post.get("author_id") else None,
#         "author_username": post.get("author_username", "unknown"),
#         "caption": post.get("caption", ""),
#         "media_url": post.get("media_url"),
#         "media_type": post.get("media_type"),
#         "likes_count": int(post.get("likes_count", 0)),
#         "comments_count": int(post.get("comments_count", 0)),
#         "saves_count": int(post.get("saves_count", 0)),
#         "created_at": created_iso,
#     }

#     # camelCase mirrors (frontend-friendly)
#     out.update({
#         "authorUsername": out["author_username"],
#         "mediaUrl": out["media_url"],
#         "mediaType": out["media_type"],
#         "likesCount": out["likes_count"],
#         "commentsCount": out["comments_count"],
#         "savesCount": out["saves_count"],
#         "createdAt": out["created_at"],
#     })

#     return out

# def create_post(author_id: str, author_username: str, caption: str, media_url: str | None, media_type: str | None = None):
#     db = get_db()
#     doc = {
#         "author_id": ObjectId(author_id),
#         "author_username": author_username,
#         "caption": caption or "",
#         "media_url": media_url or None,      # absolute url
#         "media_type": media_type or None,
#         "likes_count": 0,
#         "comments_count": 0,
#         "saves_count": 0,
#         "created_at": datetime.utcnow(),
#     }
#     res = db.posts.insert_one(doc)
#     doc["_id"] = res.inserted_id
#     return doc

from datetime import datetime
from bson import ObjectId
from app.extensions import get_db


def _oid(value: str):
    try:
        return ObjectId(value)
    except Exception:
        return None


def serialize_post(post: dict, user_id: str | None = None) -> dict:
    created = post.get("created_at")
    post_id = str(post["_id"])

    base = {
        "_id": post_id,
        "author_id": str(post.get("author_id")) if post.get("author_id") else None,
        "author_username": post.get("author_username", "unknown"),
        "caption": post.get("caption", ""),
        "media_url": post.get("media_url"),
        "media_type": post.get("media_type"),
        "likes_count": int(post.get("likes_count", 0) or 0),
        "comments_count": int(post.get("comments_count", 0) or 0),
        "saves_count": int(post.get("saves_count", 0) or 0),
        "created_at": created.isoformat() if created else None,

        # camelCase mirrors (frontend friendly)
        "authorUsername": post.get("author_username", "unknown"),
        "mediaUrl": post.get("media_url"),
        "mediaType": post.get("media_type"),
        "likesCount": int(post.get("likes_count", 0) or 0),
        "commentsCount": int(post.get("comments_count", 0) or 0),
        "savesCount": int(post.get("saves_count", 0) or 0),
        "createdAt": created.isoformat() if created else None,
    }

    if user_id:
        db = get_db()
        uo = _oid(user_id)
        po = _oid(post_id)
        base["is_liked"] = bool(db.likes.find_one({"user_id": uo, "post_id": po}))
        base["is_saved"] = bool(db.saves.find_one({"user_id": uo, "post_id": po}))
        base["isLiked"] = base["is_liked"]
        base["isSaved"] = base["is_saved"]
    else:
        base["is_liked"] = False
        base["is_saved"] = False
        base["isLiked"] = False
        base["isSaved"] = False

    return base


def create_post(author_id: str, author_username: str, caption: str, media_url: str | None, media_type: str | None):
    db = get_db()
    doc = {
        "author_id": _oid(author_id),
        "author_username": author_username,
        "caption": caption or "",
        "media_url": media_url or None,
        "media_type": media_type or None,
        "likes_count": 0,
        "comments_count": 0,
        "saves_count": 0,
        "created_at": datetime.utcnow(),
    }
    res = db.posts.insert_one(doc)
    doc["_id"] = res.inserted_id
    return doc