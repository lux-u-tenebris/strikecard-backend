#!/usr/bin/env bash

if [ ! -e ".env" ]; then
  echo "Run install.sh and configure .env file first." >&2
  exit 1
fi

source ./.env

python manage.py test
