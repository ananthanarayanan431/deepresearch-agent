#!/bin/bash

# Stop the script if any command fails
set -e

# Optional: activate virtual environment if you use one
if [ -d ".venv" ]; then
  source .venv/bin/activate
fi

# Run Uvicorn server
uvicorn deepresearch.interface.main:app --reload --host 0.0.0.0 --port 8000
