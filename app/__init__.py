"""
Orbix Backend Application Package
Exposes create_app for WSGI/Gunicorn.
"""
from .main import create_app

__all__ = ["create_app"]
