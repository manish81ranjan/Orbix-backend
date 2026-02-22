"""
User service
- Profile retrieval
- Profile updates
"""

from bson import ObjectId
from app.extensions import mongo_db
from app.models.user_model import (
    get_user_by_username,
    serialize_user
)
from app.utils.validators import min_length


def get_profile_by_username(username: str):
    user = get_user_by_username(username)
    if not user:
        raise ValueError("User not found")
    return serialize_user(user)


def update_profile(user_id: str, data: dict):
    updates = {}

    if "bio" in data:
        if not min_length(data["bio"], 0):
            raise ValueError("Invalid bio")
        updates["bio"] = data["bio"]

    if "avatar" in data:
        updates["avatar"] = data["avatar"]

    if not updates:
        return None

    mongo_db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": updates}
    )

    user = mongo_db.users.find_one({"_id": ObjectId(user_id)})
    return serialize_user(user)
