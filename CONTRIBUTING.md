# Contributing to AI Development Team

First off, thank you for considering contributing to AI Development Team! It's people like you that make open-source software such an amazing way to learn, inspire, and create.

This document provides guidelines for contributing to the AI Development Team project. These are just guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Your First Code Contribution](#your-first-code-contribution)
  - [Pull Requests](#pull-requests)
- [Development Environment](#development-environment)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
  - [Testing](#testing)
- [Style Guides](#style-guides)
  - [Git Commit Messages](#git-commit-messages)
  - [Python Style Guide](#python-style-guide)
  - [Documentation Style](#documentation-style)
- [Additional Notes](#additional-notes)
  - [Issue and Pull Request Labels](#issue-and-pull-request-labels)
  - [Release Process](#release-process)

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to [your-email@example.com](mailto:your-email@example.com).

## How Can I Contribute?

### Reporting Bugs

Bugs are tracked as [GitHub issues](https://guides.github.com/features/issues/). When you create a bug report, please include the following information:

1. **A clear, descriptive title** that identifies the problem.
2. **A detailed description** of the behavior you observed and what you expected to happen instead.
3. **Steps to reproduce** the problem.
4. **Environment details** (OS, Python version, package versions, etc.).
5. **Code samples** that demonstrate the issue, if applicable.
6. **Screenshots or logs** that show the issue, if applicable.

### Suggesting Enhancements

Enhancement suggestions are also tracked as [GitHub issues](https://guides.github.com/features/issues/). When creating an enhancement suggestion, please include:

1. **A clear, descriptive title** that describes the enhancement.
2. **A detailed description** of the suggested enhancement.
3. **Why this enhancement would be useful** to most users.
4. **Examples** of how the enhancement would be used.
5. **Any alternatives** you've considered.

### Your First Code Contribution

Unsure where to begin contributing? You can start by looking through the `good first issue` and `help wanted` issues:

- [Good first issues](https://github.com/yourusername/ai-development-team/issues?q=is:open+is:issue+label:"good+first+issue")
- [Help wanted issues](https://github.com/yourusername/ai-development-team/issues?q=is:open+is:issue+label:"help+wanted")

### Pull Requests

1. Fork the repository and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

## Development Environment

### Prerequisites

- Python 3.9+
- [Poetry](https://python-poetry.org/)
- [Git](https://git-scm.com/)

### Setup

1. **Fork** the repository on GitHub.
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/yourusername/ai-development-team.git
   cd ai-development-team
   ```
3. **Set up the development environment**:
   ```bash
   poetry install --with dev,ai,cli
   ```
4. **Activate the virtual environment**:
   ```bash
   poetry shell
   ```
5. **Install pre-commit hooks**:
   ```bash
   pre-commit install
   ```

### Testing

Run the test suite to make sure everything works:

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=ai_development_team --cov-report=term-missing

# Run a specific test file
pytest tests/test_agent.py -v
```

## Style Guides

### Git Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line
- Consider starting the commit message with an applicable emoji:
  - 🎨 `:art:` when improving the format/structure of the code
  - 🐛 `:bug:` when fixing a bug
  - 🔧 `:wrench:` when changing configuration
  - 📝 `:memo:` when writing docs
  - 🚀 `:rocket:` when improving performance
  - ✅ `:white_check_mark:` when adding tests
  - 🔒 `:lock:` when dealing with security
  - ⬆️ `:arrow_up:` when upgrading dependencies
  - ⬇️ `:arrow_down:` when downgrading dependencies

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use type hints for all function signatures
- Use docstrings for all public modules, functions, classes, and methods
- Keep lines to a maximum of 88 characters (Black's default)
- Use absolute imports

### Documentation Style

- Use [Google-style docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
- Document all public APIs
- Include examples in docstrings where helpful
- Keep documentation up to date with code changes

## Additional Notes

### Issue and Pull Request Labels

- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Improvements or additions to documentation
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention is needed
- `question`: Further information is requested
- `wontfix`: This will not be worked on

### Release Process

1. Update the version in `pyproject.toml`
2. Update `CHANGELOG.md` with the new version
3. Create a pull request with these changes
4. After merging, create a new release on GitHub
5. The release will trigger the publish workflow

## Thank You!

Your contributions to open source, large or small, make great projects like this possible. Thank you for taking the time to contribute.
