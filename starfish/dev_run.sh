#!/usr/bin/env bash

if [ ! -e ".env" ]; then
  echo "Run install.sh and configure .env file first." >&2
  exit 1
fi

set -e

PORT="${1:-8000}"
if [[ $# -gt 0 ]]; then shift; fi

source ./.env
python manage.py runserver 0.0.0.0:$PORT
