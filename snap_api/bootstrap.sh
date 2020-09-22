#!/bin/sh

# export FLASK_APP=./index.py
source $(pipenv --venv)/bin/activate

# flask run -h 0.0.0.0 -p $PORT
gunicorn --bind :$PORT --workers 1 --threads 1  --timeout 0 index:app