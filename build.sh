#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install system dependencies required for psycopg2
apt-get update && apt-get install -y \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate
