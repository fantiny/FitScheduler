#!/bin/sh

# Wait for database to be ready
echo "Waiting for database to be ready..."
python -m app.utils.wait_for_db

# Run migrations
echo "Running database migrations..."
alembic upgrade head

# Start application
echo "Starting application..."
exec "$@" 