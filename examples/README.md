# Code Generator Examples

This directory contains examples demonstrating how to use the Code Generator module.

## Prerequisites

- Python 3.9+
- Dependencies installed (run from project root):
  ```bash
  pip install -e .
  ```

## Examples

### 1. Basic Usage

Demonstrates how to generate a simple calculator module with functions and a class.

**Run with:**
```bash
python examples/basic_usage.py
```

**Expected Output:**
- Creates a `generated/calculator.py` file with the calculator implementation
- Prints the generated code to the console

### 2. Template Example

Shows how to use templates for code generation, including creating a template and using it to generate code.

**Run with:**
```bash
python examples/template_example.py
```

**Expected Output:**
- Creates a `generated/Person.py` file with a generated Person class
- Prints the generated code to the console

## How to Run Examples

1. Navigate to the project root directory
2. Install the package in development mode if you haven't already:
   ```bash
   pip install -e .
   ```
3. Run the example scripts directly with Python

## Creating Your Own Examples

1. Create a new Python file in this directory
2. Import the CodeGenerator:
   ```python
   from ai_development_team.core import CodeGenerator, CodeArtifact
   ```
3. Use the generator to create code artifacts
4. Save the artifacts to disk using the `save()` method

## Notes

- The `generated` directory will be created automatically
- You can safely delete the `generated` directory at any time - it will be recreated when running the examples again
