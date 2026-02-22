from flask import Blueprint, jsonify
from app.extensions import get_db

health_bp = Blueprint("health", __name__)


@health_bp.route("", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "orbix-backend"}), 200


@health_bp.route("/db", methods=["GET"])
def health_db():
    try:
        db = get_db()
        db.command("ping")
        return jsonify({"status": "ok", "db": "connected"}), 200
    except Exception as e:
        return jsonify({"status": "fail", "db": "not_connected", "error": str(e)}), 500
