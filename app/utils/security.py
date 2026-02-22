import jwt
from datetime import datetime, timedelta
from flask import current_app


def _parse_expiry(exp: str) -> timedelta:
    """
    Supports: '7d', '12h', '30m', '900s'
    Default: 7 days
    """
    if not exp:
        return timedelta(days=7)

    val = str(exp).strip().lower()

    try:
        if val.endswith("d"):
            return timedelta(days=int(val[:-1]))
        if val.endswith("h"):
            return timedelta(hours=int(val[:-1]))
        if val.endswith("m"):
            return timedelta(minutes=int(val[:-1]))
        if val.endswith("s"):
            return timedelta(seconds=int(val[:-1]))
        # if it's a plain number, treat as days
        return timedelta(days=int(val))
    except Exception:
        return timedelta(days=7)


def create_jwt(user_id: str) -> str:
    expires_in = current_app.config.get("JWT_EXPIRES_IN", "7d")
    exp_delta = _parse_expiry(expires_in)

    payload = {
        "sub": user_id,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + exp_delta
    }

    return jwt.encode(payload, current_app.config["JWT_SECRET"], algorithm="HS256")


def decode_jwt(token: str):
    return jwt.decode(token, current_app.config["JWT_SECRET"], algorithms=["HS256"])
