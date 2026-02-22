#!/usr/bin/env bash
# Render start script for Orbix backend

set -o errexit

# Start Gunicorn
gunicorn wsgi:app \
  --bind 0.0.0.0:${PORT:-5000} \
  --workers 2 \
  --threads 4 \
  --timeout 120
