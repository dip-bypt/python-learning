#!/usr/bin/env bash
# Helper script to run day15 locally.
# Usage: ./run_day15.sh <OPENROUTER_API_KEY>

if [ -n "$1" ]; then
  export OPENROUTER_API_KEY="$1"
  python3 "$(dirname "$0")/day15.py"
else
  # If a .env file exists in this folder, source it (simple parser for KEY=VALUE)
  if [ -f "$(dirname "$0")/.env" ]; then
    echo "Loading .env from $(dirname "$0")/.env"
    # shellcheck disable=SC1090
    set -o allexport
    # shellcheck disable=SC1091
    source "$(dirname "$0")/.env"
    set +o allexport
    python3 "$(dirname "$0")/day15.py"
  else
    echo "Usage: $0 <OPENROUTER_API_KEY>"
    echo "Or create a day15/.env file with OPENROUTER_API_KEY and run: $0"
  fi
fi
