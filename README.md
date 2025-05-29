# AI Development Team

An autonomous AI development team that can build software based on high-level requirements through specialized AI agents working together.

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

- Python 3.9+
- Git
- pip (Python package manager)
- Docker & Docker Compose (for containerized development)

### Local Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ai-development-team.git
   cd ai-development-team
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install the package in development mode:
   ```bash
   pip install -e ".[dev]"
   ```

4. Set up pre-commit hooks:
   ```bash
   pre-commit install
   ```

### Docker Development Setup

1. Build and start the development container:
   ```bash
   ./dev.sh build
   ./dev.sh start
   ```

2. Access the container shell:
   ```bash
   ./dev.sh shell
   ```

3. Stop the container when done:
   ```bash
   ./dev.sh stop
   ```

## 🛠️ Usage

### 🚀 AI Development Team

A framework for building autonomous AI development teams that can understand requirements and generate software through iterative development cycles.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

## 🎯 Features

- **🤖 Autonomous Agents**: AI agents that understand requirements, design systems, and write code
- **🧩 Modular Architecture**: Extensible with new agent types and capabilities
- **💻 CLI Interface**: Intuitive command-line interface for development workflows
- **📂 Project Management**: Built-in project structure and management
- **🔄 Iterative Development**: Continuous improvement through feedback cycles

## 🚀 Quick Start

### Installation

```bash
# Install from source
git clone https://github.com/yourusername/ai-development-team.git
cd ai-development-team
pip install -e .[all]
```

### Basic Usage

1. **Create a new project**:
   ```bash
   aidev project create my_project --description "My awesome project"
   ```

2. **Navigate to project directory**:
   ```bash
   cd my_project
   ```

3. **Start development workflow**:
   ```bash
   aidev workflow start .
   ```

4. **Analyze requirements**:
   ```bash
   aidev workflow analyze .
   ```

5. **Generate system design**:
   ```bash
   aidev workflow design .
   ```

## 🏗️ Project Structure

```
ai_development_team/
├── core/                  # Core functionality
│   ├── __init__.py
│   ├── agent.py          # Base agent implementation
│   ├── project.py        # Project management
│   └── workflow.py       # Development workflow orchestration
├── interfaces/           # User interfaces
│   └── cli/              # Command-line interface
│       ├── __init__.py
│       └── main.py       # CLI entry point
├── models/               # Data models
├── utils/                # Utility functions
│   ├── __init__.py
│   └── logging.py        # Logging configuration
└── tests/                # Test suite
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

- **Black** for code formatting
- **isort** for import sorting
- **flake8** for linting
- **mypy** for static type checking

Run all checks:

```bash
black .
isort .
flake8
mypy .
```

### Pre-commit Hooks

Pre-commit hooks are configured to automatically format and check your code before each commit. Install with:

```bash
pre-commit install
```

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

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

## 🙏 Acknowledgments

- Inspired by the vision of autonomous AI development teams
- Built with ❤️ by the open-source community
- Thanks to all contributors who have helped shape this project

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

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on how to get started.

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
