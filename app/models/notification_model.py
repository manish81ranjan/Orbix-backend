from datetime import datetime
from bson import ObjectId
from app.extensions import get_db


def _oid(value: str):
    try:
        return ObjectId(value)
    except Exception:
        return None


def serialize_notification(n: dict) -> dict:
    created = n.get("created_at")
    return {
        "_id": str(n["_id"]),
        "user_id": str(n.get("user_id")) if n.get("user_id") else None,
        "from_user_id": str(n.get("from_user_id")) if n.get("from_user_id") else None,
        "from_username": n.get("from_username"),
        "type": n.get("type"),
        "message": n.get("message"),
        "read": n.get("read", False),
        "created_at": created.isoformat() if created else None
    }


def create_notification(user_id: str, from_user_id: str | None, from_username: str | None, notif_type: str, message: str):
    user_oid = _oid(user_id)
    if not user_oid:
        raise ValueError("Invalid user_id")

    from_oid = _oid(from_user_id) if from_user_id else None
    db = get_db()

    doc = {
        "user_id": user_oid,
        "from_user_id": from_oid,
        "from_username": from_username,
        "type": notif_type,
        "message": message,
        "read": False,
        "created_at": datetime.utcnow()
    }
    res = db.notifications.insert_one(doc)
    doc["_id"] = res.inserted_id
    return doc


def get_notifications_for_user(user_id: str, limit: int = 50):
    user_oid = _oid(user_id)
    if not user_oid:
        raise ValueError("Invalid user_id")

    db = get_db()
    cursor = db.notifications.find({"user_id": user_oid}).sort("created_at", -1).limit(limit)
    return list(cursor)


def mark_all_read(user_id: str):
    user_oid = _oid(user_id)
    if not user_oid:
        raise ValueError("Invalid user_id")

    db = get_db()
    db.notifications.update_many({"user_id": user_oid, "read": False}, {"$set": {"read": True}})
    return True
