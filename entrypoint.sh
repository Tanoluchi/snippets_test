#!/bin/sh
set -e

run_manage_py() {
    python3 manage.py "$@"
}

# Apply database migration
echo "===============Apply database migrations==============="
run_manage_py makemigrations
run_manage_py migrate

# Collect static files
echo "===============Collect static files==============="
run_manage_py collectstatic --noinput

# Start server
echo "===============Starting server==============="
run_manage_py runserver "0.0.0.0:8000"