"""
Notification service
- Fetch notifications
- Mark all read
"""

from app.models.notification_model import (
    get_notifications_for_user,
    serialize_notification,
    mark_all_read
)


def get_user_notifications(user: dict, limit: int = 50):
    items = get_notifications_for_user(str(user["_id"]), limit)
    return [serialize_notification(n) for n in items]


def mark_notifications_read(user: dict):
    mark_all_read(str(user["_id"]))
    return {"ok": True}
