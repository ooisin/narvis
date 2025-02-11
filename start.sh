#! /usr/bin/env bash

set -e
set -x

python backend/app/db_connection_check.py
python backend/app/initial_data.py

uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
