# Technical Writer Agent

The `TechnicalWriterAgent` is a specialized agent responsible for managing and generating technical documentation across the project. It ensures documentation quality, consistency, and accessibility.

## Table of Contents
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Features](#features)
- [CLI Commands](#cli-commands)
- [API Reference](#api-reference)
- [Configuration](#configuration)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)

## Installation

The `TechnicalWriterAgent` is included in the main package. No additional installation is required.

```bash
# Ensure you have the main package installed
pip install -e .
```

## Quick Start

```python
from agent_core.agents.technical_writer import TechnicalWriterAgent

# Initialize the agent
docs_agent = TechnicalWriterAgent(config={
    "doc_formats": ["markdown", "html"],
    "doc_style": "google",
    "include_examples": True
})

# Generate documentation
response = await docs_agent.generate_documentation(
    target_path="path/to/your/code",
    output_format="markdown"
)
print(response.content)
```

## Features

### Documentation Generation
- Generates comprehensive API documentation
- Supports multiple output formats (Markdown, HTML)
- Includes code examples and usage guides
- Maintains consistent style across documentation

### Documentation Validation
- Validates existing documentation for completeness
- Checks for broken links and references
- Ensures code examples are up-to-date
- Verifies documentation coverage

### README Management
- Automatically updates project README files
- Generates table of contents
- Includes installation and usage instructions
- Maintains contribution guidelines

## CLI Commands

The Technical Writer agent can be accessed through the following CLI commands:

### Generate Documentation

```bash
# Generate Markdown documentation
ai-dev-team docs generate path/to/source --format markdown --output docs/

# Generate HTML documentation
ai-dev-team docs generate path/to/source --format html --output docs/html
```

### Validate Documentation

```bash
# Validate documentation in a directory
ai-dev-team docs validate path/to/docs

# Show detailed validation results
ai-dev-team docs validate --verbose path/to/docs
```

### Update README

```bash
# Update project README
ai-dev-team docs update-readme

# Specify custom project root
ai-dev-team docs update-readme --project-root path/to/project
```

## API Reference

### `TechnicalWriterAgent`

#### `__init__(config: Optional[Dict[str, Any]] = None)`
Initialize the TechnicalWriterAgent.

**Parameters:**
- `config`: Configuration dictionary with optional keys:
  - `doc_formats`: List of supported documentation formats (default: `["markdown"]`)
  - `doc_style`: Documentation style guide (default: `"google"`)
  - `include_examples`: Whether to include code examples (default: `True`)

#### `generate_documentation(target_path: str, output_format: str = "markdown", output_dir: Optional[str] = None) -> AgentMessage`
Generate documentation for the specified target.

**Parameters:**
- `target_path`: Path to the target file or package to document
- `output_format`: Output format (e.g., 'markdown', 'html')
- `output_dir`: Directory where documentation will be generated

**Returns:**
- `AgentMessage` with generation results and metadata

#### `validate_documentation(target_path: str) -> AgentMessage`
Validate existing documentation.

**Parameters:**
- `target_path`: Path to the target file or directory to validate

**Returns:**
- `AgentMessage` with validation results and findings

#### `update_readme(project_root: str = ".") -> AgentMessage`
Update the project's README file.

**Parameters:**
- `project_root`: Root directory of the project

**Returns:**
- `AgentMessage` with update results

## Configuration

The Technical Writer agent can be configured using a YAML configuration file:

```yaml
documentation:
  formats:
    - markdown
    - html
  style: google
  include_examples: true
  templates:
    readme: templates/README.md.j2
    api: templates/api.md.j2
```

## Examples

### Basic Usage

```python
from agent_core.agents.technical_writer import TechnicalWriterAgent

# Initialize with custom configuration
docs_agent = TechnicalWriterAgent({
    "doc_formats": ["markdown", "rst"],
    "doc_style": "numpy",
    "include_examples": False
})

# Generate API documentation
response = await docs_agent.generate_documentation(
    target_path="src/my_package",
    output_format="markdown",
    output_dir="docs/api"
)

# Validate documentation
validation = await docs_agent.validate_documentation("docs")
print(validation.metadata["warnings"])

# Update README
await docs_agent.update_readme("path/to/project")
```

## Troubleshooting

### Common Issues

#### Documentation Generation Fails
- **Symptom**: `Failed to generate documentation` error
- **Solution**: Ensure the target path exists and contains valid Python code

#### Validation Warnings
- **Symptom**: Many validation warnings about missing docstrings
- **Solution**: Run with `--fix` to automatically add missing docstrings

#### README Not Updating
- **Symptom**: README changes aren't being applied
- **Solution**: Check file permissions and ensure the project root is correct

### Debugging

To enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Or from the command line:

```bash
ai-dev-team --log-level DEBUG docs generate ...
```
