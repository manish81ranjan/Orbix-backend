"""
Follow service
- Follow / unfollow users
"""

from app.models.follow_model import follow, unfollow
from app.models.user_model import get_user_by_id


def follow_user(current_user: dict, target_user_id: str):
    target = get_user_by_id(target_user_id)
    if not target:
        raise ValueError("Target user not found")

    res = follow(str(current_user["_id"]), target_user_id)
    if not res:
        return {"followed": False, "message": "Already following or invalid"}

    return {"followed": True, "message": "Followed successfully"}


def unfollow_user(current_user: dict, target_user_id: str):
    target = get_user_by_id(target_user_id)
    if not target:
        raise ValueError("Target user not found")

    ok = unfollow(str(current_user["_id"]), target_user_id)
    return {"unfollowed": ok, "message": "Unfollowed" if ok else "Not following"}
