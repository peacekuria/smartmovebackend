#!/bin/bash
set -e

# Run Flask database migrations
flask db upgrade

# Start Gunicorn
exec gunicorn --bind 0.0.0.0:$PORT wsgi:app
