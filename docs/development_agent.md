# Development Agent

The `DevelopmentAgent` is a specialized agent designed to handle various software development tasks including requirements analysis, code generation, and code review.

## Table of Contents
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Features](#features)
- [API Reference](#api-reference)
- [Configuration](#configuration)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)

## Installation

The `DevelopmentAgent` is included in the main package. No additional installation is required.

```bash
# Ensure you have the main package installed
pip install -e .
```

## Quick Start

```python
from agent_core.agents.development.agent import DevelopmentAgent

# Initialize the agent
dev_agent = DevelopmentAgent(config={
    "name": "MyDevAgent",
    "skills": ["python", "javascript"]
})

# Analyze requirements
requirements = "Create a REST API endpoint for user authentication"
analysis = dev_agent.analyze_requirements(requirements)

# Generate code
code, metadata = dev_agent.generate_code(requirements)
print(code)
```

## Features

### Requirements Analysis
- Parses natural language requirements
- Identifies key components and dependencies
- Generates structured output for further processing

### Code Generation
- Generates code based on requirements
- Supports multiple programming languages
- Includes relevant documentation and type hints

### Code Review
- Analyzes existing code
- Provides feedback on code quality
- Suggests improvements and best practices

### Knowledge Management
- Maintains context between operations
- Tracks tasks and their status
- Stores relevant information for future reference

## API Reference

### `DevelopmentAgent`

#### `__init__(config: Optional[Dict[str, Any]] = None, **kwargs)`
Initialize the DevelopmentAgent.

**Parameters:**
- `config`: Configuration dictionary
- `**kwargs`: Additional keyword arguments (will be merged into config)

#### `analyze_requirements(requirements: str) -> Dict[str, Any]`
Analyze and structure requirements.

**Parameters:**
- `requirements`: Natural language requirements

**Returns:**
- Dictionary containing structured requirements

#### `generate_code(task: str, context: Optional[Dict] = None) -> Tuple[str, Dict]`
Generate code based on the given task.

**Parameters:**
- `task`: Description of what code to generate
- `context`: Additional context for code generation

**Returns:**
- Tuple of (generated_code, metadata)

#### `write_code(file_path: str, code: str, overwrite: bool = False) -> bool`
Write code to a file.

**Parameters:**
- `file_path`: Path to the file to write
- `code`: Code content to write
- `overwrite`: Whether to overwrite existing files

**Returns:**
- Boolean indicating success

#### `review_code(code: str, language: str = "python") -> Dict[str, Any]`
Review the given code.

**Parameters:**
- `code`: Code to review
- `language`: Programming language of the code

**Returns:**
- Dictionary containing review feedback

## Configuration

The `DevelopmentAgent` can be configured using the following options:

```python
config = {
    "name": "MyDevAgent",  # Agent name
    "skills": ["python", "javascript"],  # List of programming languages
    "verbose": True,  # Enable verbose output
    "auto_format": True  # Auto-format generated code
}

agent = DevelopmentAgent(config=config)
```

## Examples

### Basic Code Generation

```python
from agent_core.agents.development.agent import DevelopmentAgent

agent = DevelopmentAgent()
code, _ = agent.generate_code("Create a function that calculates factorial")
print(code)
```

### File Operations

```python
from pathlib import Path

# Write code to a file
file_path = Path("factorial.py")
success = agent.write_code(str(file_path), code)

if success:
    print(f"Code written to {file_path}")
```

## Troubleshooting

### Common Issues

1. **ImportError: No module named 'agent_core'**
   Ensure you've installed the package in development mode:
   ```bash
   pip install -e .
   ```

2. **AttributeError: 'DevelopmentAgent' object has no attribute 'role'**
   Make sure you're using the latest version of the codebase.

3. **FileExistsError when writing files**
   Use `overwrite=True` when calling `write_code()` if you want to overwrite existing files.

### Getting Help

For additional help, please [open an issue](https://github.com/yourusername/ai-development-team/issues) with:
- A description of the problem
- Steps to reproduce
- Expected vs. actual behavior
- Any error messages or logs
