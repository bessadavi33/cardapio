#!/bin/bash
echo "Starting Flask app with Gunicorn..."
gunicorn app:app --bind 0.0.0.0:$PORT
