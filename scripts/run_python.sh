#!/bin/bash
# This script ensures Python commands are executed consistently across environments
# by automatically handling virtual environment activation and Python alias issues.

# Exit on error
set -e

# Check if this script is being sourced (it shouldn't be)
if [[ "${BASH_SOURCE[0]}" != "${0}" ]]; then
  echo "⚠️  This script should be executed, not sourced."
  return 1
fi

# Check if we're in the project directory
PROJECT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || echo "")
if [ -z "$PROJECT_ROOT" ]; then
  # Try to find project root another way
  SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
  PROJECT_ROOT=$(dirname "$SCRIPT_DIR")
fi

# Navigate to project root
cd "$PROJECT_ROOT" || { echo "❌ Could not find project root"; exit 1; }

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
  echo "❌ Virtual environment not found. Please run ./setup.sh first."
  exit 1
fi

# Activate virtual environment if not already activated
if [ -z "$VIRTUAL_ENV" ]; then
  echo "ℹ️  Activating virtual environment..."
  source .venv/bin/activate
fi

# Ensure python command is available
if ! command -v python &> /dev/null; then
  echo "ℹ️  Creating python -> python3 alias"
  alias python=python3
fi

# Check Python version
PYTHON_VERSION=$(python --version 2>&1 | cut -d' ' -f2)
echo "🐍 Using Python $PYTHON_VERSION"

# Execute the command
echo "🚀 Running: python $*"
python "$@"
