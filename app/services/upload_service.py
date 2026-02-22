# """
# Upload service
# - Placeholder for media uploads
# - In production you should use Cloudinary or S3 signed URLs
# """

# def get_signature():
#     # Placeholder response (frontend expects endpoint to exist)
#     return {
#         "provider": "none",
#         "message": "Upload service not configured yet"
#     }


# def save_upload_metadata(user: dict, payload: dict):
#     # Placeholder: later save into MongoDB (uploads collection)
#     return {
#         "saved": False,
#         "message": "Upload metadata not stored yet",
#         "payload": payload
#     }
import os
import uuid
import cloudinary
import cloudinary.uploader
from werkzeug.utils import secure_filename

ALLOWED_IMAGE = {"png", "jpg", "jpeg", "webp", "gif"}
ALLOWED_VIDEO = {"mp4", "webm", "mov", "m4v"}

def _ext(filename: str) -> str:
    return (filename.rsplit(".", 1)[-1] or "").lower()

def _media_type(filename: str) -> str:
    e = _ext(filename)
    if e in ALLOWED_IMAGE:
        return "image"
    if e in ALLOWED_VIDEO:
        return "video"
    return "unknown"

def upload_file(file_storage):
    """
    Uploads to Cloudinary if env is set, otherwise saves locally (dev).
    Returns: (url, media_type)
    """
    if not file_storage or not file_storage.filename:
        raise ValueError("No file provided")

    filename = secure_filename(file_storage.filename)
    mtype = _media_type(filename)
    if mtype == "unknown":
        raise ValueError("Only images/videos are allowed")

    # ✅ Cloudinary (Render-friendly)
    cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME")
    api_key = os.getenv("CLOUDINARY_API_KEY")
    api_secret = os.getenv("CLOUDINARY_API_SECRET")

    if cloud_name and api_key and api_secret:
        cloudinary.config(cloud_name=cloud_name, api_key=api_key, api_secret=api_secret, secure=True)

        public_id = f"orbix/{uuid.uuid4().hex}"
        resource_type = "video" if mtype == "video" else "image"

        result = cloudinary.uploader.upload(
            file_storage,
            public_id=public_id,
            resource_type=resource_type,
            folder="orbix",
        )
        return result.get("secure_url"), mtype

    # ✅ Local fallback (dev)
    upload_dir = os.path.join(os.getcwd(), "uploads")
    os.makedirs(upload_dir, exist_ok=True)

    unique = f"{uuid.uuid4().hex}_{filename}"
    path = os.path.join(upload_dir, unique)
    file_storage.save(path)

    # Your backend should serve /uploads static
    return f"/uploads/{unique}", mtype
