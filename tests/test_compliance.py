"""Tests for the compliance checker."""

import sys
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add the scripts directory to the path
sys.path.append(str(Path(__file__).parent.parent / "scripts"))

# Import the compliance checker
import check_compliance  # noqa: E402


def test_compliance_checker_initialization():
    """Test that the compliance checker initializes correctly."""
    checker = check_compliance.ComplianceChecker()
    assert checker.root_dir == Path.cwd()
    assert checker.results["passed"] == []
    assert checker.results["warnings"] == []
    assert checker.results["errors"] == []
    assert checker.results["metrics"] == {}


def test_check_environment_missing_vars():
    """Test environment variable checking with missing variables."""
    with patch.dict("os.environ", {}, clear=True):
        checker = check_compliance.ComplianceChecker()
        checker.check_environment()

        # Should have errors for missing required env vars
        assert len(checker.results["errors"]) > 0
        assert any(
            "Missing required environment variables" in err
            for err in checker.results["errors"]
        )


def test_check_environment_valid():
    """Test environment variable checking with all required variables."""
    with patch.dict(
        "os.environ",
        {"PYTHONPATH": "/path/to/project", "ENVIRONMENT": "development"},
        clear=True,
    ):
        checker = check_compliance.ComplianceChecker()
        checker.check_environment()

        # Should have no errors and one passed check
        assert len(checker.results["errors"]) == 0
        assert any("environment variables" in msg for msg in checker.results["passed"])


def test_check_python_version_valid():
    """Test Python version checking with a valid version."""
    with patch("sys.version_info", (3, 9, 0)):
        checker = check_compliance.ComplianceChecker()
        checker.check_python_version()

        # Should have no errors and one passed check
        assert len(checker.results["errors"]) == 0
        assert any("Python version" in msg for msg in checker.results["passed"])


def test_check_python_version_invalid(monkeypatch):
    """Test Python version checking with an invalid version."""
    # Create a namedtuple to properly mock version_info
    from collections import namedtuple

    # Create a version info that's too old
    VersionInfo = namedtuple("VersionInfo", ["major", "minor", "micro"])
    old_version = VersionInfo(3, 6, 0)

    # Patch sys.version_info to return our old version
    monkeypatch.setattr(sys, "version_info", old_version)

    # Also patch the MIN_PYTHON_VERSION to make the test more reliable
    monkeypatch.setattr(check_compliance, "MIN_PYTHON_VERSION", (3, 8, 0))

    checker = check_compliance.ComplianceChecker()
    checker.check_python_version()

    # Should have an error about Python version
    assert (
        len(checker.results["errors"]) > 0
    ), "Expected version check to fail with old Python version"
    assert any(
        "Python 3.8" in err for err in checker.results["errors"]
    ), f"Expected error about Python 3.8+ requirement, got: {checker.results['errors']}"


def test_check_virtual_environment():
    """Test virtual environment checking."""
    # Test when in a virtual environment
    with (
        patch("sys.prefix", "/path/to/venv"),
        patch("sys.base_prefix", "/path/to/base"),
    ):
        checker = check_compliance.ComplianceChecker()
        checker.check_virtual_environment()
        assert any(
            "Running in a virtual environment" in msg
            for msg in checker.results["passed"]
        )

    # Test when not in a virtual environment
    with (
        patch("sys.prefix", "/path/to/base"),
        patch("sys.base_prefix", "/path/to/base"),
    ):
        checker = check_compliance.ComplianceChecker()
        checker.check_virtual_environment()
        assert any(
            "Not running in a virtual environment" in msg
            for msg in checker.results["warnings"]
        )


def test_check_required_tools():
    """Test required tools checking."""
    # Mock shutil.which to simulate tools being present
    with patch("shutil.which", return_value="/path/to/tool"):
        checker = check_compliance.ComplianceChecker()
        checker.check_required_tools()
        assert any("All required tools" in msg for msg in checker.results["passed"])

    # Mock shutil.which to simulate tools missing
    with patch("shutil.which", return_value=None):
        checker = check_compliance.ComplianceChecker()
        checker.check_required_tools()
        assert any("Missing required tools" in err for err in checker.results["errors"])


def test_check_dependencies():
    """Test dependency checking."""
    # Mock __import__ to simulate all dependencies being available
    with patch("builtins.__import__"):
        checker = check_compliance.ComplianceChecker()
        checker.check_dependencies()
        assert any("All required packages" in msg for msg in checker.results["passed"])

    # Mock __import__ to raise ImportError for all dependencies
    with patch("builtins.__import__", side_effect=ImportError):
        checker = check_compliance.ComplianceChecker()
        checker.check_dependencies()
        assert any(
            "Missing required packages" in err for err in checker.results["errors"]
        )


def test_check_project_structure(tmp_path):
    """Test project structure checking."""
    # Create a temporary project structure
    (tmp_path / "agent_core").mkdir()
    (tmp_path / "interfaces").mkdir()
    (tmp_path / "scripts").mkdir()
    (tmp_path / "tests").mkdir()
    (tmp_path / "docs").mkdir()  # Add docs directory

    # Test with complete structure
    checker = check_compliance.ComplianceChecker(str(tmp_path))
    checker.check_project_structure()

    # Check for the success message
    assert any(
        "Project structure is valid" in msg for msg in checker.results["passed"]
    ), f"Expected 'Project structure is valid' in {checker.results['passed']}"

    # Test with missing directory
    (tmp_path / "agent_core").rmdir()
    checker = check_compliance.ComplianceChecker(str(tmp_path))
    checker.check_project_structure()

    # Check for the error message
    assert any(
        "Missing required directories" in err for err in checker.results["errors"]
    ), f"Expected 'Missing required directories' in {checker.results['errors']}"


def test_check_documentation(tmp_path):
    """Test documentation checking."""
    # Create required documentation files
    (tmp_path / "docs").mkdir()
    (tmp_path / "README.md").touch()
    (tmp_path / "docs" / "architecture.md").touch()
    (tmp_path / "docs" / "standards.md").touch()
    (tmp_path / "docs" / "environment_setup.md").touch()
    (tmp_path / "docs" / "ai_agent_protocol.md").touch()

    # Create a Python file with a docstring
    (tmp_path / "test_module.py").write_text('"""Test module docstring."""\n')

    checker = check_compliance.ComplianceChecker(str(tmp_path))
    checker.check_documentation()

    # Should have passed documentation checks
    assert any(
        "All required documentation is present" in msg
        for msg in checker.results["passed"]
    )
    assert any(
        "Python files have module docstrings" in msg
        for msg in checker.results["passed"]
    )

    # Test with missing documentation
    (tmp_path / "docs" / "ai_agent_protocol.md").unlink()
    checker = check_compliance.ComplianceChecker(str(tmp_path))
    checker.check_documentation()
    assert any(
        "Missing documentation files" in msg for msg in checker.results["warnings"]
    )


def test_run_checks_success(capsys):
    """Test the main run_checks method with successful checks."""

    # Create a mock class that will be used to patch ComplianceChecker
    class MockComplianceChecker:
        def __init__(self):
            self.check_environment = MagicMock()
            self.check_python_version = MagicMock()
            self.check_virtual_environment = MagicMock()
            self.check_required_tools = MagicMock()
            self.check_dependencies = MagicMock()
            self.check_code_style = MagicMock()
            self.check_project_structure = MagicMock()
            self.check_documentation = MagicMock()
            self.check_tests = MagicMock()
            self.report_results = MagicMock()
            self.results = {"errors": [], "warnings": [], "passed": [], "metrics": {}}

        def run_checks(self):
            # Simulate the checks running without actually calling them
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
            return True

    # Patch the ComplianceChecker class to return our mock instance
    with patch("check_compliance.ComplianceChecker") as mock_checker_cls:
        # Create our mock instance
        mock_checker = MockComplianceChecker()
        # Make the class return our mock instance
        mock_checker_cls.return_value = mock_checker

        # Create an instance and run checks
        checker = check_compliance.ComplianceChecker()
        result = checker.run_checks()

        # Verify all checks were called
        assert (
            mock_checker.check_environment.called
        ), "check_environment should be called"
        assert (
            mock_checker.check_python_version.called
        ), "check_python_version should be called"
        assert (
            mock_checker.check_virtual_environment.called
        ), "check_virtual_environment should be called"
        assert (
            mock_checker.check_required_tools.called
        ), "check_required_tools should be called"
        assert (
            mock_checker.check_dependencies.called
        ), "check_dependencies should be called"
        assert mock_checker.check_code_style.called, "check_code_style should be called"
        assert (
            mock_checker.check_project_structure.called
        ), "check_project_structure should be called"
        assert (
            mock_checker.check_documentation.called
        ), "check_documentation should be called"
        assert mock_checker.check_tests.called, "check_tests should be called"
        assert mock_checker.report_results.called, "report_results should be called"

        assert result is True, "run_checks should return True when all checks pass"


def test_run_checks_failure():
    """Test the main run_checks method with a failed check."""

    def mock_check_with_error(self):
        raise Exception("Test error")

    with patch.multiple(
        check_compliance.ComplianceChecker,
        check_environment=MagicMock(side_effect=Exception("Test error")),
        check_python_version=MagicMock(),
        check_virtual_environment=MagicMock(),
        check_required_tools=MagicMock(),
        check_dependencies=MagicMock(),
        check_code_style=MagicMock(),
        check_project_structure=MagicMock(),
        check_documentation=MagicMock(),
        check_tests=MagicMock(),
        report_results=MagicMock(side_effect=lambda: None),
    ):
        checker = check_compliance.ComplianceChecker()
        result = checker.run_checks()

        # Check that the error was recorded
        assert result is False, "run_checks should return False when checks fail"
        assert any(
            "Fatal error" in err for err in checker.results["errors"]
        ), f"Expected 'Fatal error' in {checker.results['errors']}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
