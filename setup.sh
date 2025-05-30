#!/bin/bash
set -e

echo "🚀 Setting up development environment..."

# Check if Python 3.9+ is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher and try again."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c "import sys; print('.'.join(map(str, sys.version_info[:3])))")
MAJOR_VERSION=$(echo "$PYTHON_VERSION" | cut -d. -f1)
MINOR_VERSION=$(echo "$PYTHON_VERSION" | cut -d. -f2)
if [ "$MAJOR_VERSION" -lt 3 ] || { [ "$MAJOR_VERSION" -eq 3 ] && [ "$MINOR_VERSION" -lt 9 ]; }; then
    echo "❌ Python 3.9+ is required, but you have $PYTHON_VERSION. Please upgrade your Python installation."
    exit 1
fi

echo "✅ Found Python $PYTHON_VERSION"

# Use the new venv_utils.py to manage the virtual environment
echo "🔧 Setting up virtual environment..."

# Create the virtual environment if it doesn't exist
if ! python3 -c "from scripts import venv_utils; venv_utils.create_venv()"; then
    echo "❌ Failed to create virtual environment"
    exit 1
fi

# Get the virtual environment directory
VENV_DIR=$(python3 -c 'from scripts.venv_utils import get_venv_dir; print(get_venv_dir())')

# Check if we're in the correct virtual environment
if ! python3 -c "from scripts import venv_utils; exit(0 if venv_utils.is_project_venv_activated() else 1)"; then
    echo "⚠️  Virtual environment is not activated."
    echo "   Please run: source $VENV_DIR/bin/activate"
    echo "   Then run this script again."
    exit 1
fi

echo "✅ Virtual environment is active at $VENV_DIR"
echo "Using Python from: $(which python3)"

# Upgrade pip
echo "⬆️  Upgrading pip..."
python3 -m pip install --upgrade pip

# Install dependencies
echo "📦 Installing dependencies..."
python3 -m pip install -e ".[dev]"

# Create a .python-version file for pyenv if not exists
if [ ! -f ".python-version" ]; then
    python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" > .python-version
    echo "✅ Created .python-version file"
fi

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
echo ""
echo "⚠️ IMPORTANT: Always use the virtual environment to ensure consistent Python behavior"
echo ""
