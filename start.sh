#! /usr/bin/env bash

set -e
set -x

python app/db_connection_check.py
python app/initial_data.py

uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
