from datetime import datetime
from bson import ObjectId
from app.extensions import get_db


def _oid(value: str):
    try:
        return ObjectId(value)
    except Exception:
        return None


def is_following(follower_id: str, following_id: str) -> bool:
    follower_oid = _oid(follower_id)
    following_oid = _oid(following_id)
    if not follower_oid or not following_oid:
        return False

    db = get_db()
    return db.follows.find_one({"follower_id": follower_oid, "following_id": following_oid}) is not None


def follow(follower_id: str, following_id: str):
    if follower_id == following_id:
        return None

    follower_oid = _oid(follower_id)
    following_oid = _oid(following_id)
    if not follower_oid or not following_oid:
        raise ValueError("Invalid ids")

    db = get_db()

    if is_following(follower_id, following_id):
        return None

    doc = {"follower_id": follower_oid, "following_id": following_oid, "created_at": datetime.utcnow()}
    db.follows.insert_one(doc)

    db.users.update_one({"_id": follower_oid}, {"$inc": {"following_count": 1}})
    db.users.update_one({"_id": following_oid}, {"$inc": {"followers_count": 1}})
    return doc


def unfollow(follower_id: str, following_id: str) -> bool:
    follower_oid = _oid(follower_id)
    following_oid = _oid(following_id)
    if not follower_oid or not following_oid:
        return False

    db = get_db()
    res = db.follows.delete_one({"follower_id": follower_oid, "following_id": following_oid})

    if res.deleted_count:
        db.users.update_one({"_id": follower_oid}, {"$inc": {"following_count": -1}})
        db.users.update_one({"_id": following_oid}, {"$inc": {"followers_count": -1}})

    return res.deleted_count > 0
