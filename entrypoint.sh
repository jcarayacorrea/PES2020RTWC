#!/bin/bash
set -e

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Start the server
echo "Starting server..."
python manage.py runserver 0.0.0.0:8000
