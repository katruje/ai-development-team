#!/usr/bin/env python3
"""
Check the Python environment for common issues.
"""
import platform
import sys
import subprocess
from pathlib import Path


def print_header(title):
    print(f"\n{'='*80}")
    print(f"{title:^80}")
    print(f"{'='*80}")


def check_python_version():
    """Check Python version meets minimum requirements."""
    print_header("PYTHON VERSION")
    print(f"Python {sys.version}")
    print(f"Platform: {platform.platform()}")
    print(f"Executable: {sys.executable}")

    # Check minimum Python version
    min_version = (3, 9)
    if sys.version_info < min_version:
        print(f"❌ Python {'.'.join(map(str, min_version))}+ is required")
        return False
    print("✅ Python version meets minimum requirements")
    return True


def check_virtual_environment():
    """Check if running in a virtual environment."""
    print_header("VIRTUAL ENVIRONMENT")

    in_venv = hasattr(sys, "real_prefix") or (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    )
    if in_venv:
        print(f"✅ Running in a virtual environment: {sys.prefix}")
        return True

    print("⚠️  Not running in a virtual environment")
    print("   It's recommended to use a virtual environment for development.")
    return False


def check_python_commands():
    """Check that python and python3 commands are available."""
    print_header("PYTHON COMMANDS")

    commands = ["python", "python3"]
    all_ok = True

    for cmd in commands:
        try:
            result = subprocess.run(
                [cmd, "--version"], capture_output=True, text=True, check=True
            )
            print(f"✅ {cmd}: {result.stdout.strip()}")

            # Check if it's Python 3
            if "Python 3" not in result.stdout:
                print(f"   ⚠️  {cmd} does not point to Python 3")
                all_ok = False

        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"❌ {cmd}: Command not found")
            all_ok = False

    return all_ok


def check_required_tools():
    """Check that required tools are installed."""
    print_header("REQUIRED TOOLS")

    tools = ["git", "docker", "docker-compose"]
    all_ok = True

    for tool in tools:
        try:
            result = subprocess.run(
                ["which", tool], capture_output=True, text=True, check=True
            )
            print(f"✅ {tool}: {result.stdout.strip()}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"❌ {tool}: Not found")
            all_ok = False

    return all_ok


def check_python_packages():
    """Check that required Python packages are installed."""
    print_header("PYTHON PACKAGES")

    required_packages = [
        "pytest",
        "pytest-cov",
        "pytest-mock",
        "pytest-asyncio",

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

    missing_packages = []
    for pkg in required_packages:
        try:
            __import__(pkg.replace("-", "_"))
            print(f"✅ {pkg}")
        except ImportError:
            print(f"❌ {pkg}: Not installed")
            missing_packages.append(pkg)

    if missing_packages:
        print("\nTo install missing packages, run:")
        print(f"  pip install {' '.join(missing_packages)}")
        return False

    return True


def check_project_structure():
    """Check that the project structure is correct."""
    print_header("PROJECT STRUCTURE")

    required_dirs = [
        "agent_core",
        "interfaces",
        "scripts",
        "tests",
    ]

    all_ok = True
    for dir_name in required_dirs:
        path = Path(dir_name)
        if path.exists() and path.is_dir():
            print(f"✅ {dir_name}/")
        else:
            print(f"❌ {dir_name}/: Directory not found")
            all_ok = False

    return all_ok


def main():
    """Run all environment checks."""
    print_header("ENVIRONMENT CHECK")
    print(f"Project: {Path(__file__).parent.parent.name}")
    print(f"Working directory: {Path.cwd()}")

    checks = [
        ("Python Version", check_python_version()),
        ("Virtual Environment", check_virtual_environment()),
        ("Python Commands", check_python_commands()),
        ("Required Tools", check_required_tools()),
        ("Python Packages", check_python_packages()),
        ("Project Structure", check_project_structure()),
    ]

    print_header("SUMMARY")
    all_ok = all(ok for _, ok in checks)

    for name, ok in checks:
        status = "✅" if ok else "❌"
        print(f"{status} {name}")

    if all_ok:
        print("\n🎉 All checks passed! Your environment is ready for development.")
    else:
        print("\n❌ Some checks failed. Please address the issues above.")

    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
