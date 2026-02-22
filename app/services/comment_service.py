"""
Comment service
- Add comment
- Get comments for a post
"""

from app.models.comment_model import (
    create_comment,
    get_comments_for_post,
    serialize_comment
)
from app.models.post_model import get_post_by_id


def add_comment_to_post(user: dict, post_id: str, text: str):
    if not text or not text.strip():
        raise ValueError("Comment cannot be empty")

    post = get_post_by_id(post_id)
    if not post:
        raise ValueError("Post not found")

    comment = create_comment(
        post_id=post_id,
        author_id=str(user["_id"]),
        author_username=user["username"],
        text=text.strip()
    )
    return serialize_comment(comment)


def get_post_comments(post_id: str, limit: int = 50):
    post = get_post_by_id(post_id)
    if not post:
        raise ValueError("Post not found")

    comments = get_comments_for_post(post_id, limit)
    return [serialize_comment(c) for c in comments]
