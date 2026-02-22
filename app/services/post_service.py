"""
Post service
- Create post
- Fetch single post
"""

from app.models.post_model import (
    create_post,
    get_post_by_id,
    serialize_post
)


def create_new_post(user: dict, caption: str, media_url: str | None):
    post = create_post(
        author_id=str(user["_id"]),
        author_username=user["username"],
        caption=caption,
        media_url=media_url
    )
    return serialize_post(post)


def get_post(post_id: str):
    post = get_post_by_id(post_id)
    if not post:
        raise ValueError("Post not found")
    return serialize_post(post)
