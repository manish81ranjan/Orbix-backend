"""
Global error handling for Orbix backend
- Converts uncaught errors to JSON responses
"""

from flask import jsonify
from werkzeug.exceptions import HTTPException


def register_error_handlers(app):
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        return jsonify({
            "message": e.description,
            "status": e.code
        }), e.code

    @app.errorhandler(Exception)
    def handle_exception(e):
        # In production, avoid leaking details
        return jsonify({
            "message": "Internal server error"
        }), 500
