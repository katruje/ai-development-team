"""
Virtual Environment Utilities for AI Development Team

This module provides centralized management of the project's virtual environment.
It ensures consistent virtual environment creation, activation, and usage.
"""
import os
import sys
import subprocess
from pathlib import Path
from typing import Optional, Tuple, List

def get_project_root() -> Path:
    """Return the absolute path to the project root directory."""
    return Path(__file__).parent.parent.resolve()

def get_venv_dir() -> Path:
    """Return the path to the virtual environment directory."""
    return get_project_root() / ".venv"

def is_venv_activated() -> bool:
    """Check if a virtual environment is currently activated."""
    return hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)

def is_project_venv_activated() -> bool:
    """Check if the project's virtual environment is activated."""
    if not is_venv_activated():
        return False
    
    venv_path = get_venv_dir().resolve()
    prefix_path = Path(sys.prefix).resolve()
    return prefix_path == venv_path or prefix_path.is_relative_to(venv_path)

def create_venv(force: bool = False) -> bool:
    """
    Create the project virtual environment if it doesn't exist.
    
    Args:
        force: If True, recreate the virtual environment if it exists
    
    Returns:
        bool: True if the virtual environment was created or already exists
    """
    venv_dir = get_venv_dir()
    
    if venv_dir.exists():
        if force:
            import shutil
            shutil.rmtree(venv_dir)
        else:
            return True
    
    try:
        subprocess.run(
            [sys.executable, "-m", "venv", str(venv_dir)],
            check=True,
            capture_output=True,
            text=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to create virtual environment: {e}", file=sys.stderr)
        print(f"Stdout: {e.stdout}", file=sys.stderr)
        print(f"Stderr: {e.stderr}", file=sys.stderr)
        return False

def ensure_venv() -> bool:
    """Ensure the project virtual environment exists and is active."""
    if not get_venv_dir().exists():
        print("Creating virtual environment...")
        if not create_venv():
            return False
    
    if not is_project_venv_activated():
        print("Virtual environment is not activated.")
        print(f"Please run: source {get_venv_dir()}/bin/activate")
        return False
    
    return True

def run_in_venv(command: List[str], **kwargs) -> subprocess.CompletedProcess:
    """
    Run a command in the project's virtual environment.
    
    Args:
        command: The command to run as a list of strings
        **kwargs: Additional arguments to subprocess.run()
    
    Returns:
        subprocess.CompletedProcess: The result of the command
    """
    venv_bin = get_venv_dir() / "bin"
    env = os.environ.copy()
    env["PATH"] = f"{venv_bin}{os.pathsep}{env.get('PATH', '')}"
    
    return subprocess.run(
        command,
        env=env,
        **kwargs
    )

def install_dependencies() -> bool:
    """Install project dependencies in the virtual environment."""
    if not ensure_venv():
        return False
    
    project_root = get_project_root()
    result = run_in_venv(
        ["pip", "install", "-e", ".[dev]"],
        cwd=project_root,
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"Failed to install dependencies: {result.stderr}", file=sys.stderr)
        return False
    
    print("Dependencies installed successfully.")
    return True

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Manage project virtual environment")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Create subcommand
    create_parser = subparsers.add_parser("create", help="Create the virtual environment")
    create_parser.add_argument("--force", action="store_true", help="Recreate if it already exists")
    
    # Check subcommand
    subparsers.add_parser("check", help="Check if virtual environment is active")
    
    # Install subcommand
    subparsers.add_parser("install", help="Install project dependencies")
    
    args = parser.parse_args()
    
    if args.command == "create":
        success = create_venv(force=args.force)
        if success:
            print(f"Virtual environment created at {get_venv_dir()}")
        else:
            print("Failed to create virtual environment", file=sys.stderr)
            sys.exit(1)
    elif args.command == "check":
        if is_project_venv_activated():
            print(f"✓ Virtual environment is active: {sys.prefix}")
            sys.exit(0)
        else:
            print("✗ Virtual environment is not active or incorrect", file=sys.stderr)
            sys.exit(1)
    elif args.command == "install":
        if not install_dependencies():
            sys.exit(1)
