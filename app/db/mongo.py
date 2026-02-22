from bson import ObjectId
from app.extensions import mongo_db


def get_db():
    """
    Returns the active MongoDB database object
    """
    return mongo_db


def to_objectid(value: str):
    """
    Safely convert string -> ObjectId
    Returns None if invalid
    """
    try:
      return ObjectId(value)
    except Exception:
      return None
