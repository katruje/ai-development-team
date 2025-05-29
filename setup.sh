#!/bin/bash
set -e

echo "🚀 Setting up development environment..."

# Check if Python 3.9+ is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher and try again."
    exit 1
fi

# Create and activate virtual environment
echo "🔧 Creating virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt
pip install -e ".[dev]"

# Install pre-commit hooks
echo "🔍 Setting up pre-commit hooks..."
pre-commit install

echo ""
echo "✨ Setup complete!"
echo "To activate the virtual environment, run:"
echo "  source .venv/bin/activate"
echo ""
echo "To run tests:"
echo "  pytest"
echo ""
echo "To run the application:"
echo "  python -m interfaces.cli.main start"
