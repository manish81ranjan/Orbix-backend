# from flask import Blueprint, jsonify, g
# from app.middleware.auth_required import auth_required

# from app.services.follow_service import follow_user, unfollow_user

# follow_bp = Blueprint("follows", __name__)


# @follow_bp.route("/<target_user_id>", methods=["POST"])
# @auth_required
# def follow(target_user_id):
#     try:
#         res = follow_user(g.current_user, target_user_id)
#         return jsonify(res), 200
#     except ValueError as e:
#         return jsonify({"message": str(e)}), 404


# @follow_bp.route("/<target_user_id>", methods=["DELETE"])
# @auth_required
# def unfollow(target_user_id):
#     try:
#         res = unfollow_user(g.current_user, target_user_id)
#         return jsonify(res), 200
#     except ValueError as e:
#         return jsonify({"message": str(e)}), 404
from flask import Blueprint, jsonify, g
from bson import ObjectId
from datetime import datetime

from app.middleware.auth_required import auth_required
from app.extensions import get_db
from app.models.notification_model import create_notification

follow_bp = Blueprint("follows", __name__, url_prefix="/api/follows")


def _oid(v):
    try:
        return ObjectId(str(v))
    except Exception:
        return None


@follow_bp.post("/<username>")
@auth_required
def follow_user(username):
    db = get_db()
    me = _oid(g.user_id)
    if not me:
        return jsonify({"error": "Invalid user id"}), 400

    target = db.users.find_one({"username": username})
    if not target:
        return jsonify({"error": "User not found"}), 404

    target_id = target["_id"]
    if target_id == me:
        return jsonify({"error": "You cannot follow yourself"}), 400

    # idempotent follow
    exists = db.follows.find_one({"follower_id": me, "following_id": target_id})
    if exists:
        return jsonify({"ok": True}), 200

    db.follows.insert_one(
        {"follower_id": me, "following_id": target_id, "created_at": datetime.utcnow()}
    )

    # counters
    db.users.update_one({"_id": me}, {"$inc": {"following_count": 1}})
    db.users.update_one({"_id": target_id}, {"$inc": {"followers_count": 1}})

    # notification
    create_notification(
        user_id=str(target_id),
        from_user_id=str(me),
        from_username=getattr(g, "username", None),
        notif_type="follow",
        message="started following you"
    )

    return jsonify({"ok": True}), 200


@follow_bp.post("/<username>/unfollow")
@auth_required
def unfollow_user(username):
    db = get_db()
    me = _oid(g.user_id)
    if not me:
        return jsonify({"error": "Invalid user id"}), 400

    target = db.users.find_one({"username": username})
    if not target:
        return jsonify({"error": "User not found"}), 404

    target_id = target["_id"]

    deleted = db.follows.delete_one({"follower_id": me, "following_id": target_id}).deleted_count
    if deleted:
        db.users.update_one({"_id": me}, {"$inc": {"following_count": -1}})
        db.users.update_one({"_id": target_id}, {"$inc": {"followers_count": -1}})

    return jsonify({"ok": True}), 200