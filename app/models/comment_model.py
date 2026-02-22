# from datetime import datetime
# from bson import ObjectId
# from app.extensions import get_db


# def _oid(value: str):
#     try:
#         return ObjectId(value)
#     except Exception:
#         return None


# def serialize_comment(c: dict) -> dict:
#     created = c.get("created_at")
#     return {
#         "_id": str(c["_id"]),
#         "post_id": str(c.get("post_id")) if c.get("post_id") else None,
#         "author_id": str(c.get("author_id")) if c.get("author_id") else None,
#         "author_username": c.get("author_username"),
#         "text": c.get("text", ""),
#         "created_at": created.isoformat() if created else None
#     }


# def create_comment(post_id: str, author_id: str, author_username: str, text: str):
#     post_oid = _oid(post_id)
#     author_oid = _oid(author_id)
#     if not post_oid or not author_oid:
#         raise ValueError("Invalid ids")

#     db = get_db()
#     doc = {
#         "post_id": post_oid,
#         "author_id": author_oid,
#         "author_username": author_username,
#         "text": text,
#         "created_at": datetime.utcnow()
#     }
#     res = db.comments.insert_one(doc)
#     doc["_id"] = res.inserted_id

#     db.posts.update_one({"_id": post_oid}, {"$inc": {"comments_count": 1}})
#     return doc


# def get_comments_for_post(post_id: str, limit: int = 50):
#     post_oid = _oid(post_id)
#     if not post_oid:
#         raise ValueError("Invalid post_id")

#     db = get_db()
#     cursor = db.comments.find({"post_id": post_oid}).sort("created_at", 1).limit(limit)
#     return list(cursor)
from datetime import datetime
from bson import ObjectId
from app.extensions import get_db


def serialize_comment(c: dict) -> dict:
    created = c.get("created_at")
    created_iso = created.isoformat() if created else None

    return {
        "_id": str(c.get("_id")),
        "post_id": str(c.get("post_id")) if c.get("post_id") else None,
        "author_id": str(c.get("author_id")) if c.get("author_id") else None,
        "author_username": c.get("author_username", "unknown"),
        "text": c.get("text", ""),
        "created_at": created_iso,

        # camelCase for frontend
        "postId": str(c.get("post_id")) if c.get("post_id") else None,
        "authorUsername": c.get("author_username", "unknown"),
        "createdAt": created_iso,
    }


def add_comment(post_id: str, author_id: str, author_username: str, text: str):
    db = get_db()

    if not ObjectId.is_valid(post_id):
        raise ValueError("Invalid post_id")

    if not ObjectId.is_valid(author_id):
        raise ValueError("Invalid author_id")

    doc = {
        "post_id": ObjectId(post_id),
        "author_id": ObjectId(author_id),
        "author_username": author_username or "unknown",
        "text": text or "",
        "created_at": datetime.utcnow(),
    }

    res = db.comments.insert_one(doc)
    doc["_id"] = res.inserted_id

    # keep counts in posts
    db.posts.update_one(
        {"_id": ObjectId(post_id)},
        {"$inc": {"comments_count": 1}}
    )

    return doc


def list_comments(post_id: str, limit: int = 50):
    db = get_db()

    if not ObjectId.is_valid(post_id):
        raise ValueError("Invalid post_id")

    return list(
        db.comments.find({"post_id": ObjectId(post_id)})
        .sort("created_at", 1)
        .limit(int(limit))
    )