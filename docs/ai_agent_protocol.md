# AI Agent Protocol: Standards Compliance

This document defines the protocol for ensuring AI agents consistently follow project standards and properly utilize the provided development assets.

## Table of Contents
- [1. Introduction](#1-introduction)
- [2. Pre-Execution Verification](#2-pre-execution-verification)
- [3. Runtime Verification](#3-runtime-verification)
- [4. Post-Execution Verification](#4-post-execution-verification)
- [5. Standard Operating Procedures](#5-standard-operating-procedures-sops)
- [6. Documentation Requirements](#6-documentation-requirements)
- [7. Continuous Integration Checks](#7-continuous-integration-checks)
- [8. Agent Training and Calibration](#8-agent-training-and-calibration)
- [9. Compliance Monitoring](#9-compliance-monitoring)
- [10. Incident Response](#10-incident-response)

## 1. Introduction

This protocol ensures all AI agents in the development environment:

1. Adhere to established coding standards
2. Properly utilize the provided development tools and scripts
3. Maintain consistent behavior across different environments
4. Document their actions and decisions appropriately
5. Follow security and best practices

## 2. Pre-Execution Verification

Before any code execution, AI agents must:

### 2.1 Environment Validation

```python
def validate_environment():
    """Verify the environment meets all requirements."""
    # Check Python version
    if not (3, 9) <= sys.version_info < (4, 0):
        raise EnvironmentError("Python 3.9+ is required")
        
    # Verify virtual environment
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        raise EnvironmentError("Not running in a virtual environment")
    
    # Verify required tools are available
    required_tools = ['git', 'docker', 'python3']
    for tool in required_tools:
        if not shutil.which(tool):
            raise EnvironmentError(f"Required tool not found: {tool}")
```

### 2.2 Configuration Check

```python
def check_configuration():
    """Verify all required configurations are present."""
    required_config = {
        'PYTHONPATH': 'Project root directory',
        'ENVIRONMENT': 'Development/Production/Staging',
    }
    
    missing = [k for k in required_config if k not in os.environ]
    if missing:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")
```

### 2.3 Dependency Verification

```python
def verify_dependencies():
    """Ensure all required Python packages are installed."""
    required_packages = [
        'pytest', 'flake8', 'isort', 'flake8', 'mypy',
        'pydantic', 'python-dotenv', 'pyyaml', 'rich'
    ]
    
    missing = []
    for pkg in required_packages:
        try:
            __import__(pkg.replace('-', '_'))
        except ImportError:
            missing.append(pkg)
    
    if missing:
        raise ImportError(f"Missing required packages: {', '.join(missing)}")
```

## 3. Runtime Verification

During execution, agents must:

### 3.1 Standard Library Usage

- Always use pathlib.Path instead of os.path for file operations
- Use context managers for file operations
- Implement proper error handling and logging
- Use type hints for all function signatures

### 3.2 Code Style Enforcement

```python
def enforce_code_style(code: str) -> bool:
    """Verify code adheres to project style guidelines."""
    # Check with flake8
    try:
        subprocess.run(
            ['flake8', '--check', '-'],
            input=code.encode(),
            check=True,
            capture_output=True
        )
    except subprocess.CalledProcessError:
        return False
    
    # Check with flake8
    try:
        subprocess.run(
            ['flake8', '-'],
            input=code.encode(),
            check=True,
            capture_output=True
        )
    except subprocess.CalledProcessError:
        return False
        
    return True
```

### 3.3 Resource Management

- Use context managers for all resource allocation
- Implement proper cleanup in finally blocks
- Monitor memory usage and file handles
- Respect system resource limits

## 4. Post-Execution Verification

After code generation/execution:

### 4.1 Output Validation

```python
def validate_output(output: str) -> dict:
    """Validate the output meets project standards."""
    results = {
        'has_docstrings': bool(re.search(r'""".*?"""', output, re.DOTALL)),
        'has_type_hints': 'def ' in output and '->' in output,
        'has_tests': 'test_' in output or 'Test' in output,
        'code_style_valid': enforce_code_style(output)
    }
    return results
```

### 4.2 Test Generation and Execution

```python
def generate_and_run_tests(code: str) -> bool:
    """Generate and run tests for the provided code."""
    # Generate tests (simplified example)
    test_code = f"""
import unittest
from your_module import your_function

class TestYourFunction(unittest.TestCase):
    def test_basic(self):
        # Add test cases here
        pass

if __name__ == '__main__':
    unittest.main()
    """
    
    # Save and run tests
    with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as f:
        f.write(test_code.encode())
        test_file = f.name
    
    try:
        result = subprocess.run(['python', test_file], capture_output=True, text=True)
        return result.returncode == 0
    finally:
        os.unlink(test_file)
```

## 5. Standard Operating Procedures (SOPs)

### 5.1 Code Generation SOP

1. **Input Validation**
   - Verify input requirements are complete and unambiguous
   - Check for potential security issues in input
   - Validate against known patterns and constraints

2. **Code Generation**
   - Follow the project's style guide
   - Include appropriate docstrings and type hints
   - Add relevant comments for complex logic

3. **Self-Review**
   - Run static analysis tools
   - Verify all imports are used and correctly scoped
   - Check for potential bugs or edge cases

### 5.2 Documentation SOP

1. **Code Documentation**
   - Document all public APIs
   - Include examples in docstrings
   - Add type hints to all function signatures

2. **Project Documentation**
   - Update README.md for significant changes
   - Document architectural decisions in ARCHITECTURE.md
   - Keep CHANGELOG.md updated

## 6. Documentation Requirements

### 6.1 Code Documentation

```python
def example_function(param1: str, param2: int) -> bool:
    """Brief description of what the function does.
    
    Extended description with details about the function's behavior,
    edge cases, and examples.
    
    Args:
        param1: Description of the first parameter.
        param2: Description of the second parameter.
        
    Returns:
        Description of the return value.
        
    Raises:
        ValueError: If parameters are invalid.
        
    Example:
        >>> example_function("test", 42)
        True
    """
    # Function implementation
    return True
```

### 6.2 Commit Messages

Follow the Conventional Commits specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

## 7. Continuous Integration Checks

### 7.1 Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
-   repo: https://github.com/psf/flake8
    rev: 22.12.0
    hooks:
    - id: flake8
      language_version: python3.9
      
-   repo: https://github.com/pycqa/isort
    rev: 5.11.4
    hooks:
    - id: isort
      name: isort (python)
      
-   repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
    - id: flake8
      additional_dependencies: [flake8-docstrings, flake8-typing-imports]
```

### 7.2 GitHub Actions Workflow

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e .[dev]
    - name: Run tests
      run: |
        pytest --cov=your_package tests/
    - name: Check code style
      run: |
        flake8 --check .
        isort --check-only .
        flake8
        mypy .
```

## 8. Agent Training and Calibration

### 8.1 Initial Training

1. **Fine-tuning**
   - Fine-tune base models on project-specific code
   - Include examples of good and bad code patterns
   - Focus on project-specific conventions and idioms

2. **Few-shot Learning**
   - Provide multiple examples for each task type
   - Include edge cases and error handling
   - Show proper documentation patterns

### 8.2 Continuous Learning

1. **Feedback Loop**
   - Collect user feedback on AI-generated code
   - Use reinforcement learning from human feedback (RLHF)
   - Regularly update models with new examples

2. **Performance Monitoring**
   - Track code quality metrics over time
   - Monitor test coverage and success rates
   - Identify and address common failure modes

## 9. Compliance Monitoring

### 9.1 Automated Audits

```python
def run_compliance_audit():
    """Run automated compliance checks."""
    checks = [
        ('Code Style', check_code_style()),
        ('Test Coverage', check_test_coverage()),
        ('Documentation', check_documentation()),
        ('Dependencies', check_dependencies()),
        ('Security', run_security_scan())
    ]
    
    all_passed = all(passed for _, passed in checks)
    
    print("\nCompliance Report:")
    print("-" * 50)
    for name, passed in checks:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{name}: {status}")
    
    return all_passed
```

### 9.2 Reporting

1. **Daily Reports**
   - Summary of code generation activities
   - Compliance statistics
   - Identified issues and resolutions

2. **Trend Analysis**
   - Track compliance metrics over time
   - Identify patterns in code quality
   - Measure impact of improvements

## 10. Incident Response

### 10.1 Issue Triage

1. **Classification**
   - Severity assessment (Critical/High/Medium/Low)
   - Impact analysis
   - Priority assignment

2. **Containment**
   - Roll back problematic changes
   - Disable affected functionality if necessary
   - Implement workarounds

### 10.2 Post-Mortem

1. **Root Cause Analysis**
   - Timeline of events
   - Identification of contributing factors
   - Impact assessment

2. **Preventive Measures**
   - Update training data
   - Add new validation rules
   - Improve monitoring and alerts

---

This protocol should be reviewed and updated regularly to adapt to new requirements and insights from the development process.
