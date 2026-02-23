# from flask import Flask, jsonify
# from .config import Config
# from .extensions import init_extensions

# from .routes.health_routes import health_bp
# from .routes.auth_routes import auth_bp
# from .routes.user_routes import user_bp
# from .routes.post_routes import post_bp
# from .routes.comment_routes import comment_bp
# from .routes.follow_routes import follow_bp
# from .routes.notification_routes import notification_bp
# from .routes.upload_routes import upload_bp

# from .middleware.logging import register_logging
# from .middleware.error_handler import register_error_handlers
# from .db.indexes import create_indexes


# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(Config)

#     db = init_extensions(app)

#     register_logging(app)
#     register_error_handlers(app)

#     create_indexes(db)

#     app.register_blueprint(health_bp, url_prefix="/api/health")
#     app.register_blueprint(auth_bp, url_prefix="/api/auth")
#     app.register_blueprint(user_bp, url_prefix="/api/users")
#     app.register_blueprint(post_bp, url_prefix="/api/posts")
#     app.register_blueprint(comment_bp, url_prefix="/api/comments")
#     app.register_blueprint(follow_bp, url_prefix="/api/follows")
#     app.register_blueprint(notification_bp, url_prefix="/api/notifications")
#     app.register_blueprint(upload_bp, url_prefix="/api/upload")

#     @app.route("/", methods=["GET"])
#     def root():
#         return jsonify({"name": "Orbix Backend", "status": "running"}), 200

#     return app
# from fileinput import filename
# import os
# from backend import app
# from flask import Flask, jsonify, request
# from .config import Config
# from .extensions import init_extensions

# from .routes.health_routes import health_bp
# from .routes.auth_routes import auth_bp
# from .routes.user_routes import user_bp
# from .routes.post_routes import post_bp
# from .routes.comment_routes import comment_bp
# from .routes.follow_routes import follow_bp
# from .routes.notification_routes import notification_bp
# from .routes.upload_routes import upload_bp

# from .middleware.logging import register_logging
# from .middleware.error_handler import register_error_handlers
# from .db.indexes import create_indexes
# from flask import send_from_directory

# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(Config)

#     FRONTEND_ORIGIN = "http://localhost:5173"

#     # ✅ 1) Handle ALL preflight requests (OPTIONS) globally
#     @app.before_request
#     def handle_preflight():
#         if request.method == "OPTIONS":
#             return ("", 204)

#     # ✅ 2) Add CORS headers to EVERY response (even errors)
#     @app.after_request
#     def add_cors_headers(response):
#         origin = request.headers.get("Origin")
#         if origin == FRONTEND_ORIGIN:
#             response.headers["Access-Control-Allow-Origin"] = origin
#         else:
#             # optional: keep strict; or use "*" during dev
#             response.headers["Access-Control-Allow-Origin"] = FRONTEND_ORIGIN

#         response.headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,PATCH,DELETE,OPTIONS"
#         response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
#         response.headers["Access-Control-Max-Age"] = "86400"
#         return response

#     # init db/extensions
#     db = init_extensions(app)

#     register_logging(app)
#     register_error_handlers(app)
#     create_indexes(db)

#     # blueprints
#     app.register_blueprint(health_bp, url_prefix="/api/health")
#     app.register_blueprint(auth_bp, url_prefix="/api/auth")
#     app.register_blueprint(user_bp, url_prefix="/api/users")
#     app.register_blueprint(post_bp, url_prefix="/api/posts")
#     app.register_blueprint(comment_bp, url_prefix="/api/comments")
#     app.register_blueprint(follow_bp, url_prefix="/api/follows")
#     app.register_blueprint(notification_bp, url_prefix="/api/notifications")
#     app.register_blueprint(upload_bp, url_prefix="/api/upload")

#     UPLOAD_DIR = os.path.join(os.getcwd(), "uploads")
#     os.makedirs(UPLOAD_DIR, exist_ok=True)

#     @app.route("/uploads/<path:filename>")
#     def uploaded_file(filename):
#         return send_from_directory(UPLOAD_DIR, filename)
#     @app.get("/")
#     def root():
#         return jsonify({"name": "Orbix Backend", "status": "running"}), 200

#     return app
#import os


# import os
# from flask import Flask, jsonify, send_from_directory

# from app.config import Config
# from app.extensions import init_extensions

# from app.routes.auth_routes import auth_bp
# from app.routes.post_routes import post_bp
# from app.routes.upload_routes import upload_bp


# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(Config)

#     # Prevent 308 redirects (important for OPTIONS)
#     app.url_map.strict_slashes = False

#     # Upload size (fallback 25MB)
#     app.config["MAX_CONTENT_LENGTH"] = getattr(
#         Config, "MAX_CONTENT_LENGTH", 25 * 1024 * 1024
#     )

#     # ✅ Render-friendly writable folder
#     uploads_dir = os.environ.get("UPLOADS_DIR") or os.path.join("/tmp", "orbix_uploads")
#     os.makedirs(uploads_dir, exist_ok=True)
#     app.config["UPLOADS_DIR"] = uploads_dir

#     # Init Mongo + CORS
#     init_extensions(app)

#     # ✅ IMPORTANT: register WITHOUT extra url_prefix
#     # because your blueprints already include /api/... prefixes
#     app.register_blueprint(auth_bp)
#     app.register_blueprint(post_bp)
#     app.register_blueprint(upload_bp)

#     # Serve uploaded files
#     @app.get("/uploads/<path:filename>")
#     def serve_upload(filename):
#         return send_from_directory(app.config["UPLOADS_DIR"], filename)

#     @app.get("/api/health")
#     def health():
#         return jsonify({"status": "ok"}), 200

#     @app.get("/")
#     def root():
#         return jsonify({"name": "Orbix Backend", "status": "running"}), 200

#     return app
# import os
# from flask import Flask, jsonify, send_from_directory, request
# from app.config import Config
# from app.extensions import init_extensions, get_db
# from app.db.indexes import create_indexes

# from app.routes.auth_routes import auth_bp
# from app.routes.post_routes import post_bp
# from app.routes.upload_routes import upload_bp


# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(Config)

#     # Render / reverse proxy friendly
#     app.url_map.strict_slashes = False
#     app.config["MAX_CONTENT_LENGTH"] = getattr(Config, "MAX_CONTENT_LENGTH", 25 * 1024 * 1024)

#     # ---------- Extensions (Mongo + CORS) ----------
#     init_extensions(app)

#     # ---------- Indexes ----------
#     try:
#         db = get_db()
#         create_indexes(db)
#     except Exception:
#         # don't crash app if db not ready at boot
#         pass

#     # ---------- Uploads dir (Render friendly) ----------
#     # Render ephemeral disk -> use /tmp (works on Render)
#     uploads_dir = os.environ.get("UPLOADS_DIR") or os.path.join("/tmp", "orbix_uploads")
#     os.makedirs(uploads_dir, exist_ok=True)
#     app.config["UPLOADS_DIR"] = uploads_dir

#     @app.route("/uploads/<path:filename>")
#     def serve_upload(filename):
#         return send_from_directory(app.config["UPLOADS_DIR"], filename)

#     # ---------- Blueprints ----------
#     app.register_blueprint(auth_bp)     # expected url_prefix inside file
#     app.register_blueprint(post_bp)     # /api/posts...
#     app.register_blueprint(upload_bp)   # /api/upload...

#     @app.get("/api/health")
#     def health():
#         return jsonify({"status": "ok"}), 200

#     # ---------- Always return JSON ----------
#     @app.errorhandler(Exception)
#     def handle_any_error(e):
#         return jsonify({"error": str(e)}), 500

#     return app
# import os
# from flask import Flask, app, jsonify, send_from_directory
# from werkzeug.exceptions import HTTPException

# from app.config import Config
# from app.extensions import init_extensions, get_db
# from app.db.indexes import create_indexes

# from app.routes.auth_routes import auth_bp
# from app.routes.post_routes import post_bp
# from app.routes.upload_routes import upload_bp
# from app.routes.notification_routes import notification_bp
# from app.routes.user_routes import user_bp
# from app.routes.follow_routes import follow_bp
# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(Config)

#     # Render / reverse proxy friendly
#     app.url_map.strict_slashes = False

#     # upload limits
#     app.config["MAX_CONTENT_LENGTH"] = getattr(
#         Config, "MAX_CONTENT_LENGTH", 25 * 1024 * 1024
#     )

#     # ---------- Extensions (Mongo + CORS) ----------
#     init_extensions(app)

#     # ---------- Uploads dir (Render friendly) ----------
#     # ✅ Single source of truth: UPLOADS_DIR
#     # - Render disk is ephemeral so /tmp is safe
#     uploads_dir = os.environ.get("UPLOADS_DIR") or os.path.join("/tmp", "orbix_uploads")
#     os.makedirs(uploads_dir, exist_ok=True)
#     app.config["UPLOADS_DIR"] = uploads_dir

#     # ✅ Keep compatibility with upload_routes.py (if it uses UPLOAD_FOLDER)
#     # We'll map UPLOAD_FOLDER to the same directory
#     app.config["UPLOAD_FOLDER"] = uploads_dir

#     @app.route("/uploads/<path:filename>")
#     def serve_upload(filename):
#         return send_from_directory(app.config["UPLOADS_DIR"], filename)

#     # ---------- Indexes ----------
#     try:
#         db = get_db()
#         create_indexes(db)
#     except Exception:
#         # don't crash app if db not ready at boot
#         pass

#     # ---------- Blueprints ----------
#     app.register_blueprint(auth_bp)     # /api/auth...
#     app.register_blueprint(post_bp)     # /api/posts...
#     app.register_blueprint(upload_bp)   # /api/upload...
#     app.register_blueprint(notification_bp)
#     app.register_blueprint(user_bp)
#     app.register_blueprint(follow_bp)

#     @app.get("/api/health")
#     def health():
#         return jsonify({"status": "ok"}), 200

#     # ---------- Always return JSON (but keep correct HTTP codes) ----------
#     @app.errorhandler(Exception)
#     def handle_any_error(e):
#         if isinstance(e, HTTPException):
#             return jsonify({"error": e.description}), e.code
#         return jsonify({"error": str(e)}), 500


#     return app



import os
from flask import Flask, jsonify, send_from_directory
from werkzeug.exceptions import HTTPException
from flask_cors import CORS

from app.config import Config
from app.extensions import init_extensions, get_db
from app.db.indexes import create_indexes

from app.routes.auth_routes import auth_bp
from app.routes.post_routes import post_bp
from app.routes.upload_routes import upload_bp
from app.routes.notification_routes import notification_bp
from app.routes.user_routes import user_bp
from app.routes.follow_routes import follow_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.url_map.strict_slashes = False

    app.config["MAX_CONTENT_LENGTH"] = getattr(
        Config, "MAX_CONTENT_LENGTH", 25 * 1024 * 1024
    )

    # ✅ CORS from ENV
    origins = [o.strip().rstrip("/") for o in Config.CORS_ORIGINS.split(",") if o.strip()]
    CORS(app, origins=origins, supports_credentials=True)

    init_extensions(app)

    uploads_dir = os.environ.get("UPLOADS_DIR") or os.path.join("/tmp", "orbix_uploads")
    os.makedirs(uploads_dir, exist_ok=True)
    app.config["UPLOADS_DIR"] = uploads_dir
    app.config["UPLOAD_FOLDER"] = uploads_dir

    @app.route("/uploads/<path:filename>")
    def serve_upload(filename):
        return send_from_directory(app.config["UPLOADS_DIR"], filename)

    try:
        db = get_db()
        create_indexes(db)
    except Exception:
        pass

    app.register_blueprint(auth_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(notification_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(follow_bp)

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok"}), 200

    @app.errorhandler(Exception)
    def handle_any_error(e):
        if isinstance(e, HTTPException):
            return jsonify({"error": e.description}), e.code
        return jsonify({"error": str(e)}), 500

    return app



# import os
# from flask import Flask, jsonify, send_from_directory
# from werkzeug.exceptions import HTTPException
# from flask_cors import CORS   # ✅ ADD THIS

# from app.config import Config
# from app.extensions import init_extensions, get_db
# from app.db.indexes import create_indexes

# from app.routes.auth_routes import auth_bp
# from app.routes.post_routes import post_bp
# from app.routes.upload_routes import upload_bp
# from app.routes.notification_routes import notification_bp
# from app.routes.user_routes import user_bp
# from app.routes.follow_routes import follow_bp


# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(Config)

#     # Render / reverse proxy friendly
#     app.url_map.strict_slashes = False

#     # Upload size limit
#     app.config["MAX_CONTENT_LENGTH"] = getattr(
#         Config, "MAX_CONTENT_LENGTH", 25 * 1024 * 1024
#     )

#     # =========================
#     # ✅ CORS CONFIGURATION
#     # =========================
#     CORS(
#         app,
#         origins=[
#             "https://orbix-frontend-1c18.vercel.app",
#             "http://localhost:5173",
#         ],
#         supports_credentials=True,
#     )

#     # ---------- Extensions (Mongo, etc.) ----------
#     init_extensions(app)

#     # ---------- Uploads dir (Render safe) ----------
#     uploads_dir = os.environ.get("UPLOADS_DIR") or os.path.join("/tmp", "orbix_uploads")
#     os.makedirs(uploads_dir, exist_ok=True)

#     app.config["UPLOADS_DIR"] = uploads_dir
#     app.config["UPLOAD_FOLDER"] = uploads_dir

#     @app.route("/uploads/<path:filename>")
#     def serve_upload(filename):
#         return send_from_directory(app.config["UPLOADS_DIR"], filename)

#     # ---------- Indexes ----------
#     try:
#         db = get_db()
#         create_indexes(db)
#     except Exception:
#         pass

#     # ---------- Blueprints ----------
#     app.register_blueprint(auth_bp)
#     app.register_blueprint(post_bp)
#     app.register_blueprint(upload_bp)
#     app.register_blueprint(notification_bp)
#     app.register_blueprint(user_bp)
#     app.register_blueprint(follow_bp)

#     @app.get("/api/health")
#     def health():
#         return jsonify({"status": "ok"}), 200

#     # ---------- Global JSON Error Handler ----------
#     @app.errorhandler(Exception)
#     def handle_any_error(e):
#         if isinstance(e, HTTPException):
#             return jsonify({"error": e.description}), e.code
#         return jsonify({"error": str(e)}), 500

#     return app


