# AI Development Team

A framework for building autonomous AI development teams that can understand requirements and generate software through iterative development cycles.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

> **Note**: This is a personal project and not currently accepting external contributions.

## ✨ Features

- 🤖 **Multi-agent System**: Specialized agents (Architect, Developer, QA) collaborating on projects
- 🏗️ **Project Analysis**: Automatic project structure and dependency analysis
- 📊 **Architecture Design**: AI-assisted system design and architecture planning
- 🔍 **Code Analysis**: Intelligent code review and quality assessment
- 🛠️ **CLI Interface**: Easy-to-use command-line interface
- 🐳 **Docker Support**: Containerized development environment
- 📦 **Modular Design**: Extensible architecture for adding new capabilities

## 🚀 Quick Start

### Prerequisites

- **macOS (recommended)** or Linux
- **Python 3.9+** (3.13+ recommended)
- **Git**
- **Docker & Docker Compose** (for containerized development)
- **Homebrew** (macOS) or appropriate package manager (Linux)

### Automated Setup (Recommended)

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd ai_development_team
   ```

2. **Run the setup script**:
   ```bash
   chmod +x dev_setup.sh
   ./dev_setup.sh
   ```
   
   This will:
   - Install required system dependencies
   - Set up a Python virtual environment
   - Install all Python dependencies
   - Configure git hooks
   - Verify the environment setup
   - Ensure Python command consistency and set up the development environment

3. **Activate the virtual environment** (if not already activated):
   ```bash
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

4. **Run the application**:
   ```bash
   ./run_app.sh
   ```

### Manual Setup

For detailed manual setup instructions, see the [Environment Setup Guide](docs/environment_setup.md).

## 🧪 Testing

Run the test suite with:

```bash
# Run all tests
./run_tests.sh

# Run a specific test file
./run_tests.sh tests/test_example.py

# Run with coverage report
pytest --cov=ai_development_team tests/
```

## 🛠 Development Tools

### Helper Scripts

This project includes several helper scripts to streamline development:

- `./run_app.sh` - Run the application with proper environment setup
- `./run_tests.sh` - Run tests with proper environment setup
- `./scripts/run_python.sh` - Run Python scripts with the correct environment
- `./scripts/check_environment.py` - Verify the development environment
- `./scripts/ensure_python.py` - Ensure Python command consistency and set up the development environment

### Code Quality

```bash
# Format code with flake8 and isort

isort .

# Check for style issues
flake8

# Run type checking
mypy .
```

## 🛠️ Development

### Prerequisites

- Python 3.9+
- [Poetry](https://python-poetry.org/) (recommended)

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/ai-development-team.git
   cd ai-development-team
   ```

2. **Install dependencies**:
   ```bash
   poetry install --with dev,ai,cli
   ```

3. **Activate the virtual environment**:
   ```bash
   poetry shell
   ```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=ai_development_team --cov-report=term-missing

# Run a specific test file
pytest tests/test_agent.py -v
```

### Code Quality

This project enforces code quality through:

- **Flake8** for code formatting
- **isort** for import sorting
- **flake8** for linting
- **mypy** for static type checking

Run all checks:

```bash

isort .
flake8
mypy .
```

### Pre-commit Hooks

Pre-commit hooks are configured to automatically format and check your code before each commit. Install with:

```bash
pre-commit install
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📚 Documentation

For detailed documentation, please visit our [Documentation](https://github.com/yourusername/ai-development-team#readme).

## 📈 Project Status

This project is currently in **active development**. Major features are being added and APIs may change.

### Upcoming Features

- [ ] Web interface for better interaction
- [ ] Integration with popular AI models
- [ ] Plugin system for extending functionality
- [ ] More agent specializations

## 🛠️ Usage

### Basic Commands

```bash
# Start the interactive CLI
python -m interfaces.cli.main start

# Show help
python -m interfaces.cli.main --help

# Work with the architect agent
python -m interfaces.cli.main architect --help
```

### Architect Agent Examples

Analyze a project:
```bash
python -m interfaces.cli.main architect analyze ./your-project --verbose
```

Show project structure:
```bash
python -m interfaces.cli.main architect structure ./your-project
```

## 🏗️ Project Structure

```
ai_development_team/
├── agent_core/           # Core AI agent implementations
│   └── agents/           # Individual agent implementations
│       └── architect/    # Architect agent
├── interfaces/           # User interfaces
│   └── cli/              # Command-line interface
├── services/             # Reusable services
├── config/               # Configuration management
├── tests/                # Test suite
├── docs/                 # Documentation
├── .windsurf/            # Development environment configuration
├── Dockerfile            # Container configuration
└── docker-compose.yml    # Service definitions
```

## 📚 Documentation

- [Architecture](./docs/architecture.md) - System architecture and design decisions
- [Development Guide](./docs/development.md) - Setting up the development environment
- [API Reference](./docs/api.md) - Detailed API documentation
- [Changelog](./CHANGELOG.md) - Development history and changes

## 🧪 Development

### Code Style

We enforce consistent code style using:
- `black` - Code formatting
- `isort` - Import sorting
- `flake8` - Linting
- `mypy` - Static type checking

### Development Scripts

We provide a `dev.sh` script to simplify common development tasks:

```bash
# Build the development container
./dev.sh build

# Start the development environment
./dev.sh start

# Run tests
./dev.sh test

# Run linters
./dev.sh lint

# Format code
./dev.sh format
```


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚙️ Workspace Configuration

This project includes a `.vscode/Windsurf.code-workspace` file with pre-configured settings for auto-approval of common development files. This helps streamline the development workflow by reducing manual approvals for standard file operations.

> **Test Note**: This update was made to verify auto-approval functionality. If you can see this note without having to approve the change, the auto-approval is working correctly!

> **Final Test**: This is a final test after updating VS Code user settings. If you can see this without approving, the configuration is working!

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=ai_development_team --cov-report=term-missing
```

### Pre-commit Hooks

Pre-commit hooks are configured to automatically format and check your code before each commit.

## Development Status

This project is currently in active development and not yet ready for production use.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
