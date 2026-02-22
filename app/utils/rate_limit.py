"""
Basic in-memory rate limiting
- Simple protection for auth & write-heavy routes
- For production at scale, replace with Redis
"""

import time
from flask import request, jsonify

# key -> [timestamps]
_REQUEST_LOG = {}


def rate_limit(max_requests=30, window_seconds=60):
    """
    Decorator for rate limiting
    Example: @rate_limit(10, 60)
    """
    def decorator(fn):
        def wrapper(*args, **kwargs):
            key = f"{request.remote_addr}:{request.endpoint}"
            now = time.time()

            timestamps = _REQUEST_LOG.get(key, [])
            timestamps = [t for t in timestamps if now - t < window_seconds]

            if len(timestamps) >= max_requests:
                return jsonify({
                    "message": "Too many requests. Please slow down."
                }), 429

            timestamps.append(now)
            _REQUEST_LOG[key] = timestamps
            return fn(*args, **kwargs)
        wrapper.__name__ = fn.__name__
        return wrapper
    return decorator
