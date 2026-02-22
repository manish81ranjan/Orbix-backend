"""
Standard API response helpers
- Keeps responses consistent across services
"""

from flask import jsonify


def success(data=None, message="success", status=200):
    return jsonify({
        "success": True,
        "message": message,
        "data": data
    }), status


def error(message="error", status=400, data=None):
    return jsonify({
        "success": False,
        "message": message,
        "data": data
    }), status
