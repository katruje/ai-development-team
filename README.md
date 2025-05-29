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
