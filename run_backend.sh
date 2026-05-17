#!/bin/bash
# Run FastAPI frontend_web server with proper path setup

cd "$(dirname "$0")" || exit 1

export PYTHONPATH="${PWD}/bb84-qkd-simulator:${PYTHONPATH}"

echo "Starting BB84 QKD FastAPI Server..."
echo "Backend available at: http://127.0.0.1:8000"
echo "Press Ctrl+C to stop"
echo ""

/Users/sasank.kotra/CNS_lab/.venv/bin/python -m uvicorn frontend_web.main:app \
  --host 127.0.0.1 \
  --port 8000 \
  --reload \
  "$@"
