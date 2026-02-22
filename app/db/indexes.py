# from pymongo import ASCENDING, DESCENDING


# def create_indexes(db):
#     db.users.create_index([("email", ASCENDING)], unique=True, name="uniq_email")
#     db.users.create_index([("username", ASCENDING)], unique=True, name="uniq_username")

#     db.posts.create_index([("created_at", DESCENDING)], name="posts_created_at_desc")
#     db.posts.create_index([("author_id", ASCENDING), ("created_at", DESCENDING)], name="posts_author_created_at")

#     db.comments.create_index([("post_id", ASCENDING), ("created_at", ASCENDING)], name="comments_post_created_at")

#     db.follows.create_index(
#         [("follower_id", ASCENDING), ("following_id", ASCENDING)],
#         unique=True,
#         name="uniq_follow_pair"
#     )

#     db.saves.create_index(
#         [("user_id", ASCENDING), ("post_id", ASCENDING)],
#         unique=True,
#         name="uniq_save_pair"
#     )

#     db.notifications.create_index(
#         [("user_id", ASCENDING), ("created_at", DESCENDING)],
#         name="notifications_user_created_at"
#     )

# from pymongo import ASCENDING, DESCENDING
# from app.extensions import get_db


# def _safe_create_index(collection, keys, **kwargs):
#     """
#     Create index if not present.
#     If same index exists with different name/options, ignore safely.
#     """
#     try:
#         collection.create_index(keys, **kwargs)
#     except Exception as e:
#         msg = str(e)
#         # If already exists with different name -> ignore
#         if "IndexOptionsConflict" in msg or "already exists with a different name" in msg:
#             return
#         # any other error -> raise
#         raise


# def create_indexes():
#     db = get_db()

#     # USERS
#     _safe_create_index(db.users, [("email", ASCENDING)], unique=True, name="uniq_email")
#     _safe_create_index(db.users, [("username", ASCENDING)], unique=True, name="uniq_username")

#     # POSTS
#     _safe_create_index(db.posts, [("author_id", ASCENDING)], name="idx_posts_author")
#     _safe_create_index(db.posts, [("created_at", DESCENDING)], name="idx_posts_created")

#     # COMMENTS
#     _safe_create_index(db.comments, [("post_id", ASCENDING), ("created_at", ASCENDING)], name="idx_comments_post_created")

#     # FOLLOWS
#     _safe_create_index(db.follows, [("follower_id", ASCENDING), ("following_id", ASCENDING)], unique=True, name="uniq_follow_pair")

#     # NOTIFICATIONS
#     _safe_create_index(db.notifications, [("user_id", ASCENDING), ("created_at", DESCENDING)], name="idx_notif_user_created")

#     # SAVES
#     _safe_create_index(db.saves, [("user_id", ASCENDING), ("post_id", ASCENDING)], unique=True, name="uniq_save_pair")
from pymongo import ASCENDING, DESCENDING
from pymongo.errors import OperationFailure

def _safe_create(collection, keys, name=None, **kwargs):
    """
    If an index exists with a different name, ignore.
    """
    try:
        collection.create_index(keys, name=name, **kwargs)
    except OperationFailure as e:
        # IndexOptionsConflict / already exists with different name
        if "already exists" in str(e) or "IndexOptionsConflict" in str(e):
            return
        raise

def create_indexes(db):
    # users
    _safe_create(db.users, [("email", ASCENDING)], unique=True, name="uniq_users_email")
    _safe_create(db.users, [("username", ASCENDING)], unique=True, name="uniq_users_username")

    # posts
    _safe_create(db.posts, [("created_at", DESCENDING)], name="idx_posts_created_at_desc")
    _safe_create(db.posts, [("author_id", ASCENDING), ("created_at", DESCENDING)], name="idx_posts_author_created")

    # comments
    _safe_create(db.comments, [("post_id", ASCENDING), ("created_at", ASCENDING)], name="idx_comments_post_created")

    # follows
    _safe_create(db.follows, [("follower_id", ASCENDING), ("following_id", ASCENDING)], unique=True, name="uniq_follows_pair")

    # notifications
    _safe_create(db.notifications, [("user_id", ASCENDING), ("created_at", DESCENDING)], name="idx_notifs_user_created")

    # saves
    _safe_create(db.saves, [("user_id", ASCENDING), ("post_id", ASCENDING)], unique=True, name="uniq_saves_pair")
