# Contributing to AI Development Team

Welcome! We're excited you're here to contribute. This document outlines the standards and processes for contributing to this project.

## Development Environment Setup

### Prerequisites
- Python 3.9+
- Docker (for containerized development)
- Git

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai_development_team
   ```

2. **Run the setup script**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Activate the virtual environment**
   ```bash
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

### Development Workflow

1. **Create a new branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow the code style (PEP 8)
   - Write tests for new features
   - Update documentation as needed

3. **Run tests**
   ```bash
   pytest
   ```

4. **Run pre-commit hooks**
   ```bash
   pre-commit run --all-files
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add new feature"
   git push origin feature/your-feature-name
   ```

6. **Create a pull request**
   - Open a pull request against the `main` branch
   - Ensure all tests pass
   - Request reviews from team members

## Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use type hints for all function signatures
- Write docstrings for all public functions and classes
- Keep functions small and focused on a single responsibility

## Testing

- Write unit tests for all new features
- Use descriptive test function names
- Test edge cases and error conditions
- Run tests before pushing code

## Docker Development

Build and run the development container:

```bash
docker-compose up --build
```

## Virtual Environment

We use `.venv` for local development. This directory is in `.gitignore` and should not be committed to version control.

To activate the virtual environment:

```bash
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

## Version Control

### Branch Naming

Use the following prefixes for branch names:
- `feature/`: New features
- `fix/`: Bug fixes
- `docs/`: Documentation changes
- `refactor/`: Code refactoring
- `test/`: Adding or improving tests
- `chore/`: Maintenance tasks

### Commit Messages

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
type(scope): short description

Longer description if needed
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Formatting, missing semicolons, etc.
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `test`: Adding missing tests
- `chore`: Updates to build process, package manager configs, etc.

## Code Review Process

1. Create a pull request
2. Request reviews from at least one team member
3. Address any feedback
4. Once approved, squash and merge your changes

## Questions?

If you have any questions, please open an issue or reach out to the team.
