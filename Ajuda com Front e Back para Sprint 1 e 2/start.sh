#!/bin/bash
echo "Starting Flask app with Gunicorn..."
gunicorn app:app
