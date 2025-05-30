# Project Standards and Conventions

This document outlines the standards and conventions for the AI Development Team project. All agents and developers should adhere to these guidelines to maintain consistency and quality across the codebase.

## Table of Contents

1. [Project Structure](#project-structure)
2. [Virtual Environment Management](#virtual-environment-management)
3. [Dependency Management](#dependency-management)
4. [Template Usage](#template-usage)
5. [Code Style and Linting](#code-style-and-linting)
6. [Documentation Standards](#documentation-standards)
7. [Git Workflow](#git-workflow)
8. [Testing Standards](#testing-standards)
9. [Environment Variables](#environment-variables)
10. [Docker Standards](#docker-standards)

## Project Structure

All projects should follow this standard structure:

```
project_root/
├── .python-version           # Python version (for pyenv)
├── .tool-versions           # Version management (for asdf)
├── pyproject.toml           # Project metadata and dependencies (PEP 621)
├── requirements/            # Split requirements files
│   ├── base.txt            # Core dependencies
│   ├── dev.txt             # Development dependencies
│   ├── test.txt            # Test dependencies
│   └── docs.txt            # Documentation dependencies
├── .venv/                   # Local virtual environment (gitignored)
├── .env                     # Environment variables (gitignored, .env.example committed)
├── docker/                  # Docker configuration
│   ├── Dockerfile
│   └── docker-compose.yml
└── Makefile                 # Common tasks
```

## Virtual Environment Management

### Python Version Requirements

This project requires Python 3.9 or higher. All development should be done within a virtual environment to ensure consistent dependency management.

### macOS Python Command Consistency

On macOS, there's typically a distinction between `python` (which may point to Python 2.x or be missing) and `python3`. To ensure consistency:

1. **Always activate the virtual environment** before running Python commands
2. **Use the consistent Python command** provided by the virtual environment
3. **Never rely on system Python** for project execution

```bash
# INCORRECT - may use system Python or fail
python script.py

# CORRECT - uses virtual environment Python with consistent behavior
source .venv/bin/activate
python script.py
```

### Creating a Virtual Environment

```bash
# Use the setup.sh script (recommended)
./setup.sh

# Or manually create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# After activation, the 'python' command will be available and point to correct version
python --version  # Should show Python 3.9+
```

### Project-Specific Python Alias

The project's `setup.sh` script automatically configures an alias in the virtual environment to ensure `python` consistently points to `python3`. This prevents "command not found: python" errors.

### Virtual Environment Activation

The virtual environment must be activated in each new terminal session:

# Activate the virtual environment
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

### Virtual Environment in IDEs

- **VS Code**: Automatically detects and activates the virtual environment in `.venv`
- **PyCharm**: Right-click on `.venv` directory → "Mark Directory as" → "Sources Root"
- **Other IDEs**: Configure to use the Python interpreter in `.venv/bin/python`

## Dependency Management

### Core Dependencies

All dependencies must be specified in `pyproject.toml` following [PEP 621](https://www.python.org/dev/peps/pep-0621/).

Example:
```toml
[build-system]
requires = ["setuptools>=42", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "ai_development_team"
version = "0.1.0"
description = "AI Development Team - Autonomous software development agents"
authors = [
    {name = "Your Name", email = "your.email@example.com"},
]
dependencies = [
    "typer>=0.9.0",
    "rich>=13.0.0",
    # Core dependencies
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",

    "isort>=5.12.0",
    "mypy>=1.0.0",
    "pylint>=2.17.0",
]
```

### Installing Dependencies

```bash
# Install all dependencies (including dev)
pip install -e ".[dev]"

# Install only production dependencies
pip install -e .


# Update dependencies
pip install --upgrade -e ".[dev]"
```

## Template Usage

### Code Generation Templates

All code generation templates should use the `.py.j2` extension and be stored in the appropriate agent's template directory:

```
agent_core/agents/<agent_name>/templates/
├── __init__.py
├── module_template.py.j2
└── test_template.py.j2
```

### Template Naming Conventions

- Use snake_case for template filenames
- Prefix test templates with `test_`
- Group related templates in subdirectories when necessary
- Document template variables in the template header

Example template header:

```python
# {{ module_name }}.py
# Generated by {{ agent_name }} on {{ timestamp }}
# Template: {{ template_path }}
# Variables:
#   - module_name: str - Name of the module
#   - author: str - Author name
#   - description: str - Module description
#   - imports: List[str] - List of import statements
#   - functions: List[Dict] - List of function definitions
#     - name: str - Function name
#     - params: List[Tuple[str, str]] - List of (param_name, param_type)
#     - return_type: str - Return type
#     - docstring: str - Function docstring
#     - body: str - Function body

"""{{ description }}"""

from typing import Any, Dict, List, Optional

{% for import_stmt in imports %}
{{ import_stmt }}
{% endfor %}

{% for func in functions %}
def {{ func.name }}({{ func.params|join(', ') }}) -> {{ func.return_type }}:
    """{{ func.docstring }}"""
    {{ func.body }}

{% endfor %}
```

## Code Style and Linting

### Code Formatting

We use `flake8` for code style enforcement and `isort` for import sorting. These are configured in `.flake8` and `pyproject.toml`.

```bash
# Format code


# Sort imports
isort .
```

### Linting

We use `pylint` and `mypy` for static analysis.

```bash
# Run pylint
pylint agent_core/ tests/

# Run mypy
mypy agent_core/ tests/
```

### Pre-commit Hooks

Pre-commit hooks are configured in `.pre-commit-config.yaml`. Install with:

```bash
pre-commit install
```

The hooks will run automatically on each commit.

## Documentation Standards

### Docstrings

All functions, classes, and modules must have Google-style docstrings.

Example:

```python
"""Module-level docstring.

This module provides functionality for X.
"""

from typing import List, Optional


def example_function(param1: str, param2: int = 42) -> bool:
    """Short description of the function.
    
    Longer description with more details about what the function does,
    any important notes, and examples.
    
    Args:
        param1: Description of the first parameter.
        param2: Description of the second parameter. Defaults to 42.
        
    Returns:
        Description of the return value.
        
    Raises:
        ValueError: If param1 is empty.
        
    Example:
        >>> example_function("test", 10)
        True
    """
    if not param1:
        raise ValueError("param1 cannot be empty")
    return True
```

### API Documentation

We use [MkDocs](https://www.mkdocs.org/) with the [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) theme for documentation.

To build the documentation:

```bash
mkdocs build
```

To serve the documentation locally:

```bash
mkdocs serve
```

## Git Workflow

### Branch Naming

- `main`: Production-ready code
- `develop`: Integration branch for features
- `feature/`: New features
- `bugfix/`: Bug fixes
- `hotfix/`: Critical bug fixes for production
- `release/`: Release preparation

### Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Types:
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `perf`: A code change that improves performance
- `test`: Adding missing tests or correcting existing tests
- `chore`: Changes to the build process or auxiliary tools

Example:

```
feat(agent): add support for Python 3.10

Add compatibility with Python 3.10 by updating type hints and dependencies.

Closes #123
```

## Testing Standards

### Writing Tests

- Tests should be in the `tests/` directory
- Test files should be named `test_*.py` or `*_test.py`
- Use `pytest` fixtures for test dependencies
- Follow the Arrange-Act-Assert pattern

Example test:

```python
import pytest

from agent_core.agents.developer.agent import DeveloperAgent


def test_developer_agent_initialization():
    """Test that DeveloperAgent initializes correctly."""
    # Arrange
    agent_name = "TestDeveloper"
    
    # Act
    agent = DeveloperAgent(name=agent_name)
    
    # Assert
    assert agent.name == agent_name
    assert agent.role == AgentRole.DEVELOPER
```

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=agent_core --cov-report=term-missing

# Run a specific test file
pytest tests/test_developer_agent.py

# Run a specific test function
pytest tests/test_developer_agent.py::test_developer_agent_initialization -v
```

## Environment Variables

All environment variables should be defined in the `.env` file and documented in `.env.example`.

Example `.env`:

```
# Application
ENVIRONMENT=development
LOG_LEVEL=INFO
PYTHONPATH=.

# API Keys (if needed)
# OPENAI_API_KEY=your-api-key
```

Example `.env.example`:

```
# Application
ENVIRONMENT=development  # or 'production'
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
PYTHONPATH=.

# API Keys (if needed)
# OPENAI_API_KEY=your-api-key
```

## Docker Standards

### Dockerfile

Use a multi-stage build to keep the final image small:

```dockerfile
# syntax=docker/dockerfile:1.4

# Build stage
FROM python:3.9-slim as builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies
COPY pyproject.toml .
RUN pip install --no-cache-dir -e .

# Final stage
FROM python:3.9-slim

WORKDIR /app

# Copy virtual environment
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application
COPY . .

# Run the application
CMD ["python", "-m", "interfaces.cli.main"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  app:
    build: .
    volumes:
      - .:/app
    environment:
      - PYTHONPATH=/app
    command: python -m interfaces.cli.main
```

### Building and Running

```bash
# Build the image
docker-compose build

# Run the container
docker-compose up
```

## Additional Resources

- [Python Packaging User Guide](https://packaging.python.org/)
- [PEP 8 -- Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
