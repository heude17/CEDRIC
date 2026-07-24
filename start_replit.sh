#!/usr/bin/env bash
set -e

pip install -q -r requirements.txt

export FLASK_APP=app:create_app
flask db upgrade

python3 app.py
