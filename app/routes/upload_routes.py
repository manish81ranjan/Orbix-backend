# from flask import Blueprint, jsonify, g, request
# from app.middleware.auth_required import auth_required

# from app.services.upload_service import get_signature, save_upload_metadata

# upload_bp = Blueprint("upload", __name__)


# @upload_bp.route("/signature", methods=["GET"])
# @auth_required
# def signature():
#     res = get_signature()
#     return jsonify(res), 200


# @upload_bp.route("", methods=["POST"])
# @auth_required
# def save_upload():
#     data = request.get_json(force=True) or {}
#     res = save_upload_metadata(g.current_user, data)
#     return jsonify(res), 200
# from flask import Blueprint, request, jsonify
# from app.middleware.auth_required import auth_required
# from app.services.upload_service import upload_file

# upload_bp = Blueprint("upload", __name__)

# @upload_bp.route("", methods=["POST"])
# @auth_required
# def upload_media():
#     """
#     multipart/form-data
#     file: image/video
#     """
#     f = request.files.get("file")
#     try:
#         url, media_type = upload_file(f)
#         return jsonify({"status": "ok", "url": url, "media_type": media_type})
#     except Exception as e:
#         return jsonify({"status": "fail", "message": str(e)}), 400
# import os
# import uuid
# from flask import Blueprint, request, jsonify
# from werkzeug.utils import secure_filename

# upload_bp = Blueprint("upload", __name__)

# ALLOWED = {"png", "jpg", "jpeg", "webp", "gif", "mp4", "webm", "mov"}

# def _ext(name: str):
#     return name.rsplit(".", 1)[-1].lower() if "." in name else ""

# @upload_bp.route("", methods=["POST", "OPTIONS"])
# def upload_file():
#     if request.method == "OPTIONS":
#         return ("", 204)

#     if "file" not in request.files:
#         return jsonify({"error": "file is required"}), 400

#     f = request.files["file"]
#     if not f.filename:
#         return jsonify({"error": "empty filename"}), 400

#     ext = _ext(f.filename)
#     if ext not in ALLOWED:
#         return jsonify({"error": f"unsupported file type: {ext}"}), 400

#     uploads_dir = os.path.join(os.getcwd(), "app", "static", "uploads")
#     os.makedirs(uploads_dir, exist_ok=True)

#     filename = secure_filename(f.filename)
#     final_name = f"{uuid.uuid4().hex}_{filename}"
#     save_path = os.path.join(uploads_dir, final_name)
#     f.save(save_path)

#     url = f"/static/uploads/{final_name}"
#     media_type = "video" if ext in {"mp4", "webm", "mov"} else "image"
#     return jsonify({"url": url, "media_type": media_type}), 201
# from flask import Blueprint, request, jsonify, current_app
# import os, uuid
# from werkzeug.utils import secure_filename

# upload_bp = Blueprint("upload", __name__, url_prefix="/api/upload")

# @upload_bp.route("/media", methods=["POST"])
# def upload_media():
#     if "file" not in request.files:
#         return jsonify({"error": "No file field. Use form-data key: file"}), 400

#     file = request.files["file"]
#     if not file or file.filename == "":
#         return jsonify({"error": "No file selected"}), 400

#     upload_dir = os.path.join(current_app.root_path, "uploads")
#     os.makedirs(upload_dir, exist_ok=True)

#     filename = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
#     file.save(os.path.join(upload_dir, filename))

#     ext = filename.split(".")[-1].lower()
#     media_type = "video" if ext in ["mp4", "mov", "webm"] else "image"

#     return jsonify({
#         "url": f"/uploads/{filename}",
#         "type": media_type
#     }), 201


# import os
# import uuid
# from flask import Blueprint, request, jsonify, current_app
# from werkzeug.utils import secure_filename

# from app.middleware.auth_required import auth_required

# upload_bp = Blueprint("upload", __name__, url_prefix="/api/upload")

# IMG = {"png", "jpg", "jpeg", "webp", "gif"}
# VID = {"mp4", "mov", "webm", "mkv"}

# def _ext(name: str) -> str:
#     return name.rsplit(".", 1)[-1].lower() if "." in name else ""

# @upload_bp.route("/media", methods=["POST", "OPTIONS"])
# @auth_required
# def upload_media():
#     if request.method == "OPTIONS":
#         return ("", 204)

#     if "file" not in request.files:
#         return jsonify({"error": "No file field. Use form-data key: file"}), 400

#     f = request.files["file"]
#     if not f or not f.filename:
#         return jsonify({"error": "No file selected"}), 400

#     e = _ext(f.filename)
#     if e not in IMG and e not in VID:
#         return jsonify({"error": "Unsupported file type"}), 400

#     media_type = "video" if e in VID else "image"

#     upload_dir = current_app.config["UPLOADS_DIR"]
#     os.makedirs(upload_dir, exist_ok=True)

#     filename = f"{uuid.uuid4().hex}_{secure_filename(f.filename)}"
#     f.save(os.path.join(upload_dir, filename))

#     # ✅ Absolute URL = always shows in frontend
#     base = request.host_url.rstrip("/")  # http://localhost:5000
#     absolute_url = f"{base}/uploads/{filename}"

#     return jsonify({"url": absolute_url, "type": media_type}), 201

import os, uuid
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from app.middleware.auth_required import auth_required

upload_bp = Blueprint("upload", __name__, url_prefix="/api/upload")

IMG = {"png", "jpg", "jpeg", "webp", "gif"}
VID = {"mp4", "mov", "webm", "mkv"}


def ext(name: str) -> str:
    return name.rsplit(".", 1)[-1].lower() if "." in name else ""


@upload_bp.route("/media", methods=["POST", "OPTIONS"])
@auth_required
def upload_media():
    if request.method == "OPTIONS":
        return ("", 204)

    if "file" not in request.files:
        return jsonify({"error": "No file field. Use form-data key: file"}), 400

    f = request.files["file"]
    if not f or f.filename == "":
        return jsonify({"error": "No file selected"}), 400

    e = ext(f.filename)
    if e not in IMG and e not in VID:
        return jsonify({"error": "Unsupported file type"}), 400

    media_type = "video" if e in VID else "image"

    upload_dir = current_app.config.get("UPLOADS_DIR") or os.path.join("/tmp", "orbix_uploads")
    os.makedirs(upload_dir, exist_ok=True)

    filename = f"{uuid.uuid4().hex}_{secure_filename(f.filename)}"
    f.save(os.path.join(upload_dir, filename))

    # ✅ IMPORTANT: always return relative URL
    return jsonify({"url": f"/uploads/{filename}", "type": media_type}), 201