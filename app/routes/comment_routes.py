from flask import Blueprint, request, jsonify, g
from app.middleware.auth_required import auth_required

from app.services.comment_service import add_comment_to_post, get_post_comments

comment_bp = Blueprint("comments", __name__)


@comment_bp.route("/<post_id>", methods=["GET"])
@auth_required
def list_comments(post_id):
    try:
        comments = get_post_comments(post_id, limit=50)
        return jsonify({"comments": comments}), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 404


@comment_bp.route("/<post_id>", methods=["POST"])
@auth_required
def add_comment(post_id):
    data = request.get_json(force=True) or {}
    text = data.get("text", "")

    try:
        comment = add_comment_to_post(g.current_user, post_id, text)
        return jsonify({"comment": comment}), 201
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
