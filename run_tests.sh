#!/bin/bash
set -e

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Virtual environment is not activated. Activating now..."
    if [ -d ".venv" ]; then
        source .venv/bin/activate
        echo "✅ Virtual environment activated"
    else
        echo "❌ No .venv directory found. Please run ./setup.sh first."
        exit 1
    fi
fi

# Ensure python refers to python3
if ! command -v python &> /dev/null; then
    echo "⚠️  'python' command not found. Creating alias to python3..."
    alias python=python3
fi

# Handle arguments - run specific tests or all tests
if [ "$#" -gt 0 ]; then
    echo "🧪 Running specific tests: $@"
    python -m pytest "$@" -v
else
    echo "🧪 Running all tests"
    python -m pytest -v
fi
