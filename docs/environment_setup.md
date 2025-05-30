# Environment Setup Guide

This guide will help you set up your development environment for the AI Development Team project.

## Prerequisites

- macOS (recommended) or Linux
- Homebrew (macOS) or appropriate package manager (Linux)
- Python 3.9+
- Git
- Docker & Docker Compose (for containerized development)

## Automated Setup (Recommended)

### 1. Clone the Repository

```bash
git clone <repository-url>
cd ai_development_team
```

### 2. Run the Setup Script

```bash
# Make the script executable
chmod +x dev_setup.sh

# Run the setup script
./dev_setup.sh
```

This will:
- Install system dependencies (if needed)
- Set up a Python virtual environment
- Install all Python dependencies
- Configure git hooks
- Verify the environment setup

## Manual Setup

### 1. Set Up Python Environment

#### macOS with Homebrew

```bash
# Install Python 3.13 (or latest 3.9+)
brew install python@3.13

# Ensure Python 3 is in your PATH
echo 'export PATH="/opt/homebrew/opt/python@3.13/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Verify Python version
python3 --version  # Should be 3.9 or higher
```

#### Linux (Ubuntu/Debian)

```bash
# Update package list
sudo apt update

# Install Python 3.9+ and pip
sudo apt install python3 python3-pip python3-venv

# Verify Python version
python3 --version  # Should be 3.9 or higher
```

### 2. Ensure Python Command Consistency

To ensure the `python` command points to Python 3, run:

```bash
python3 scripts/ensure_python.py
```

This script will:
- Check your Python installation
- Create a symlink from `python` to `python3` if needed
- Set up a virtual environment
- Install project dependencies

### 3. Create and Activate Virtual Environment (if not using the script)

```bash
# Create a virtual environment
python3 -m venv .venv

# Activate the virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
# .venv\Scripts\activate

# Verify you're using the virtual environment's Python
which python  # Should point to .venv/bin/python
```

### 4. Install Dependencies

```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install development dependencies
pip install -e ".[dev]"
```

### 5. Verify Installation

Run the environment check script:

```bash
python scripts/check_environment.py
```

All checks should pass before proceeding.

### 6. Set Up Git Hooks (Optional but Recommended)

```bash
pre-commit install
```

This will ensure code quality checks run before each commit.

## Common Issues

### Python Command Not Found

If `python` command is not found, but `python3` works, you can create an alias:

```bash
echo 'alias python=python3' >> ~/.zshrc  # or ~/.bashrc
source ~/.zshrc  # or ~/.bashrc
```

### Virtual Environment Not Activating

If you see warnings about not being in a virtual environment:

1. Make sure you've created the virtual environment:
   ```bash
   python3 -m venv .venv
   ```

2. Activate it:
   ```bash
   source .venv/bin/activate  # On macOS/Linux
   # or
   .venv\Scripts\activate    # On Windows
   ```

3. Verify activation:
   ```bash
   which python  # Should point to .venv/bin/python
   ```

### Missing Dependencies

If any Python packages are missing, install them with:

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Development Workflow

### Running Tests

```bash
# Run all tests
./run_tests.sh

# Run a specific test file
./run_tests.sh tests/test_example.py

# Run tests with coverage
pytest --cov=ai_development_team tests/
```

### Running the Application

```bash
# Run the application
./run_app.sh

# Or directly with Python
python -m ai_development_team.main
```

### Code Quality

```bash
# Format code with flake8 and isort

isort .

# Check for style issues
flake8

# Run type checking
mypy .
```

## Docker Development (Optional)

```bash
# Build and start the development container
./dev.sh build
./dev.sh start

# Access the container shell
./dev.sh shell

# Stop the container when done
./dev.sh stop
```

## Troubleshooting

### Python Version Issues

If you encounter Python version issues, ensure:

1. The correct Python version is in your PATH
2. The virtual environment is using the correct Python version
3. You've activated the virtual environment before running commands

### Permission Issues

If you encounter permission errors:

```bash
# Make scripts executable
chmod +x scripts/*.sh
chmod +x run_*.sh
```

### Environment Variables

If you need to set environment variables, create a `.env` file in the project root:

```env
# Example .env file
PYTHONPATH=.
DEBUG=true
```
