"""
Feed service
- Home feed logic
"""

from app.models.post_model import get_feed, serialize_post


def get_home_feed(page: int, limit: int, skip: int):
    posts = get_feed(page, limit, skip)
    return [serialize_post(p) for p in posts]
