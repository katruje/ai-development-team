#!/usr/bin/env python3
"""
AI Agent Compliance Checker

This script verifies that all code and configurations meet the project's
AI Agent Protocol standards.
"""

import ast
import os
import re
import sys
import shutil
import subprocess
from pathlib import Path
from typing import Optional

# Configuration
REQUIRED_ENV_VARS = {
    "PYTHONPATH": "Project root directory",
    "ENVIRONMENT": "Development/Production/Staging",
}

REQUIRED_PACKAGES = [
    "pytest",
    "pytest-cov",
    "pytest-mock",
    "pytest-asyncio",
    "flake8",
    "isort",
    "flake8",
    "mypy",
    "pre-commit",
    "pydantic",
    "python-dotenv",
    "pyyaml",
    "rich",
    "typer",
]

MIN_PYTHON_VERSION = (3, 9)


class ComplianceError(Exception):
    """Base class for compliance violations."""

    pass


class ComplianceChecker:
    """Main compliance checking class."""

    def __init__(self, root_dir: Optional[str] = None):
        """Initialize with the project root directory."""
        self.root_dir = Path(root_dir) if root_dir else Path.cwd()
        self.results = {"passed": [], "warnings": [], "errors": [], "metrics": {}}

    def run_checks(self) -> bool:
        """Run all compliance checks."""
        try:
            self.check_environment()
            self.check_python_version()
            self.check_virtual_environment()
            self.check_required_tools()
            self.check_dependencies()
            self.check_code_style()
            self.check_project_structure()
            self.check_documentation()
            self.check_tests()

            self.report_results()
            return len(self.results["errors"]) == 0

        except Exception as e:
            self._add_error(f"Fatal error during compliance check: {str(e)}")
            self.report_results()
            return False

    def _add_passed(self, message: str) -> None:
        """Add a passed check."""
        self.results["passed"].append(message)

    def _add_warning(self, message: str) -> None:
        """Add a warning."""
        self.results["warnings"].append(message)

    def _add_error(self, message: str) -> None:
        """Add an error."""
        self.results["errors"].append(message)

    def check_environment(self) -> None:
        """Check environment variables and configuration."""
        missing = [var for var in REQUIRED_ENV_VARS if var not in os.environ]
        if missing:
            self._add_error(
                f"Missing required environment variables: {', '.join(missing)}"
            )
        else:
            self._add_passed("All required environment variables are set")

    def check_python_version(self) -> None:
        """Verify Python version meets requirements."""
        if sys.version_info < MIN_PYTHON_VERSION:
            self._add_error(
                f"Python {'.'.join(map(str, MIN_PYTHON_VERSION))}+ is required. "
                f"Found {sys.version_info.major}.{sys.version_info.minor}"
            )
        else:
            self._add_passed(
                f"Python version {sys.version.split()[0]} meets requirements"
            )

    def check_virtual_environment(self) -> None:
        """Check if running in a virtual environment."""
        in_venv = hasattr(sys, "real_prefix") or (
            hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
        )
        if not in_venv:
            self._add_warning("Not running in a virtual environment")
        else:
            self._add_passed("Running in a virtual environment")

    def check_required_tools(self) -> None:
        """Check that required tools are installed."""
        tools = ["git", "docker", "python3"]
        missing = []

        for tool in tools:
            if not shutil.which(tool):
                missing.append(tool)

        if missing:
            self._add_error(f"Missing required tools: {', '.join(missing)}")
        else:
            self._add_passed("All required tools are installed")

    def check_dependencies(self) -> None:
        """Check that all required Python packages are installed."""
        missing = []
        # Mapping from PyPI name (as in REQUIRED_PACKAGES) to import name
        import_name_map = {"python-dotenv": "dotenv", "pyyaml": "yaml"}

        for pkg_pypi_name in REQUIRED_PACKAGES:
            # Use mapped import name if available, otherwise derive from PyPI name
            import_name = import_name_map.get(
                pkg_pypi_name, pkg_pypi_name.replace("-", "_")
            )
            try:
                __import__(import_name)
            except ImportError:
                missing.append(pkg_pypi_name)  # Report the PyPI name as missing

        if missing:
            self._add_error(f"Missing required packages: {', '.join(missing)}")
        else:
            self._add_passed("All required packages are installed")

    def check_code_style(self) -> None:
        """Check code style using Flake8."""
        try:
            # Run Flake8 to check code style
            result = subprocess.run(
                [
                    "flake8",
                    ".",
                    "--max-line-length=88",
                    "--exclude=.venv,__pycache__,.git",
                    "--isolated",
                    "--show-source",
                    "--per-file-ignores=agent_core/agents/developer/agent.py:E501",
                    "--per-file-ignores=interfaces/cli/commands/qa.py:E501",
                    "--per-file-ignores=examples/basic_usage.py:E501",
                    "--per-file-ignores=examples/template_example.py:E501",
                    "--per-file-ignores=interfaces/cli/commands/architect.py:E501",
                    (
                        "--per-file-ignores="
                        "interfaces/cli/commands/technical_writer/__init__.py:E501"
                    ),
                ],
                cwd=self.root_dir,
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                self._add_error(f"Flake8 issues found:\n{result.stderr}{result.stdout}")
            else:
                self._add_passed("Code style passes Flake8 checks")

        except Exception as e:
            self._add_error(f"Error running style checks: {str(e)}")

    def check_project_structure(self) -> None:
        """Verify the project structure is correct."""
        required_dirs = ["agent_core", "interfaces", "scripts", "tests", "docs"]

        missing = []
        for dir_name in required_dirs:
            if not (self.root_dir / dir_name).exists():
                missing.append(dir_name)

        if missing:
            self._add_error(f"Missing required directories: {', '.join(missing)}")
        else:
            self._add_passed("Project structure is valid")

    def check_documentation(self) -> None:
        """Check that documentation is complete."""
        required_docs = [
            "README.md",
            "docs/architecture.md",
            "docs/standards.md",
            "docs/environment_setup.md",
            "docs/ai_agent_protocol.md",
        ]

        missing = []
        for doc in required_docs:
            if not (self.root_dir / doc).exists():
                missing.append(doc)

        if missing:
            self._add_warning(f"Missing documentation files: {', '.join(missing)}")
        else:
            self._add_passed("All required documentation is present")

        # Check for docstrings in Python files
        self._check_python_docstrings()

    def _check_python_docstrings(self) -> None:
        """Check that Python files have proper docstrings."""
        python_files = list(self.root_dir.glob("**/*.py"))
        files_without_docstrings = []

        for py_file in python_files:
            if any(part.startswith((".", "__")) for part in py_file.parts):
                continue

            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    node = ast.parse(f.read())

                # Check module docstring
                if not (
                    node.body
                    and isinstance(node.body[0], ast.Expr)
                    and (
                        # For Python 3.7 and earlier
                        (hasattr(ast, 'Str') and isinstance(node.body[0].value, ast.Str))
                        or
                        # For Python 3.8+ where strings are stored in ast.Constant
                        (hasattr(ast, 'Constant') and isinstance(node.body[0].value, ast.Constant))
                    )
                ):
                    files_without_docstrings.append(
                        str(py_file.relative_to(self.root_dir))
                    )

            except Exception as e:
                self._add_warning(f"Error checking {py_file}: {str(e)}")

        if files_without_docstrings:
            files_str = ", ".join(files_without_docstrings[:5])
            msg = f"Python files without module docstrings: {files_str}"
            self._add_warning(
                msg + ("..." if len(files_without_docstrings) > 5 else "")
            )
        else:
            self._add_passed("All Python files have module docstrings")

    def check_tests(self) -> None:
        """Check that tests exist and pass."""
        test_dir = self.root_dir / "tests"

        if not test_dir.exists():
            self._add_warning("No tests directory found")
            return

        # Count test files
        test_files = list(test_dir.glob("test_*.py"))
        if not test_files:
            self._add_warning("No test files found in tests directory")
            return

        self._add_passed(f"Found {len(test_files)} test files")

        # Run tests if requested
        if "--run-tests" in sys.argv:
            self._run_tests()

    def _run_tests(self) -> None:
        """Run the test suite."""
        try:
            result = subprocess.run(
                ["pytest", "--cov=agent_core", "--cov-report=term-missing"],
                cwd=self.root_dir,
                capture_output=True,
                text=True,
            )

            if result.returncode != 0:
                self._add_error(f"Tests failed:\n{result.stderr}{result.stdout}")
            else:
                # Extract coverage information
                coverage_match = re.search(r"TOTAL\s+\d+\s+\d+\s+(\d+)%", result.stdout)
                if coverage_match:
                    coverage = int(coverage_match.group(1))
                    self.results["metrics"]["test_coverage"] = f"{coverage}%"

                    if coverage < 80:  # Example threshold
                        self._add_warning(f"Test coverage is below 80%: {coverage}%")
                    else:
                        self._add_passed(f"Test coverage: {coverage}%")

                self._add_passed("All tests passed")

        except Exception as e:
            self._add_error(f"Error running tests: {str(e)}")

    def report_results(self) -> None:
        """Print the compliance check results."""
        print("\n" + "=" * 80)
        print("COMPLIANCE CHECK RESULTS".center(80))
        print("=" * 80)

        # Print errors
        if self.results["errors"]:
            print("\n❌ ERRORS:")
            for error in self.results["errors"]:
                print(f"  • {error}")

        # Print warnings
        if self.results["warnings"]:
            print("\n⚠️  WARNINGS:")
            for warning in self.results["warnings"]:
                print(f"  • {warning}")

        # Print passed checks
        if self.results["passed"]:
            print("\n✅ PASSED CHECKS:")
            for passed in self.results["passed"]:
                print(f"  • {passed}")

        # Print metrics
        if self.results["metrics"]:
            print("\n📊 METRICS:")
            for name, value in self.results["metrics"].items():
                print(f"  • {name.replace('_', ' ').title()}: {value}")

        # Print summary
        print("\n" + "-" * 80)
        total_checks = (
            len(self.results["passed"])
            + len(self.results["warnings"])
            + len(self.results["errors"])
        )

        print(f"Total checks: {total_checks}")
        print(f"Passed: {len(self.results['passed'])}")
        print(f"Warnings: {len(self.results['warnings'])}")
        print(f"Errors: {len(self.results['errors'])}")

        if self.results["errors"]:
            print("\n❌ COMPLIANCE CHECK FAILED")
            sys.exit(1)
        else:
            print("\n✅ COMPLIANCE CHECK PASSED")
            sys.exit(0)


def main() -> None:
    """Run the compliance checker."""
    checker = ComplianceChecker()
    success = checker.run_checks()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
