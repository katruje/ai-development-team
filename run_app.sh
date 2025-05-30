#!/bin/bash
# Script to run the AI Development Team application with consistent Python environment

# Exit on error
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

# Handle arguments or use default command
if [ "$#" -gt 0 ]; then
    echo "🚀 Running AI Development Team with arguments: $*"
    python -m interfaces.cli.main "$@"
else
    echo "🚀 Running AI Development Team with default 'start' command"
    python -m interfaces.cli.main start
fi
