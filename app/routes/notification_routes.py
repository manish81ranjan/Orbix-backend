from flask import Blueprint, jsonify, g
from app.middleware.auth_required import auth_required
from app.models.notification_model import (
    get_notifications_for_user,
    serialize_notification,
    mark_all_read
)

notification_bp = Blueprint(
    "notifications",
    __name__,
    url_prefix="/api/notifications"
)


@notification_bp.route("", methods=["GET"])
@auth_required
def list_notifications():
    items = get_notifications_for_user(str(g.user_id), limit=100)
    return jsonify({
        "notifications": [serialize_notification(n) for n in items]
    }), 200


@notification_bp.route("/read-all", methods=["POST"])
@auth_required
def read_all():
    mark_all_read(str(g.user_id))
    return jsonify({"ok": True}), 200