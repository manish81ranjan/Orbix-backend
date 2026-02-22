from datetime import datetime
from bson import ObjectId
from app.extensions import get_db


def _oid(value: str):
    try:
        return ObjectId(value)
    except Exception:
        return None


def is_saved(user_id: str, post_id: str) -> bool:
    user_oid = _oid(user_id)
    post_oid = _oid(post_id)
    if not user_oid or not post_oid:
        return False

    db = get_db()
    return db.saves.find_one({"user_id": user_oid, "post_id": post_oid}) is not None


def save_post(user_id: str, post_id: str):
    user_oid = _oid(user_id)
    post_oid = _oid(post_id)
    if not user_oid or not post_oid:
        raise ValueError("Invalid ids")

    db = get_db()

    if is_saved(user_id, post_id):
        return None

    doc = {"user_id": user_oid, "post_id": post_oid, "created_at": datetime.utcnow()}
    res = db.saves.insert_one(doc)
    doc["_id"] = res.inserted_id
    return doc


def unsave_post(user_id: str, post_id: str) -> bool:
    user_oid = _oid(user_id)
    post_oid = _oid(post_id)
    if not user_oid or not post_oid:
        return False

    db = get_db()
    res = db.saves.delete_one({"user_id": user_oid, "post_id": post_oid})
    return res.deleted_count > 0


def get_saved_posts(user_id: str, limit: int = 50):
    user_oid = _oid(user_id)
    if not user_oid:
        raise ValueError("Invalid user_id")

    db = get_db()
    cursor = db.saves.find({"user_id": user_oid}).sort("created_at", -1).limit(limit)
    return list(cursor)
