#!/usr/bin/env bash

if [ ! -e ".env" ]; then
  echo "Run install.sh and configure .env file first." >&2
  exit 1
fi

source ./.env

PROFILING_OUTPUT_DIR=test_profiling_results
mkdir -p "$PROFILING_OUTPUT_DIR"

python -m cProfile -o "$PROFILING_OUTPUT_DIR/test.prof" manage.py test
