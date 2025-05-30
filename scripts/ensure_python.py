#!/usr/bin/env python3
"""
Ensure Python environment is set up correctly.
This script helps set up Python command aliases and virtual environments.
"""

import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional, Tuple


def run_command(cmd: list[str], cwd: Optional[str] = None) -> Tuple[bool, str]:
    """Run a shell command and return (success, output)."""
    try:
        result = subprocess.run(
            cmd, cwd=cwd, capture_output=True, text=True, check=True
        )
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return False, f"Command failed: {e.stderr}"
    except FileNotFoundError:
        return False, f"Command not found: {cmd[0]}"


def get_python_version(python_cmd: str) -> Optional[Tuple[int, int, int]]:
    """Get Python version as (major, minor, patch) or None if not found."""
    success, output = run_command([python_cmd, "--version"])
    if not success:
        return None

    # Extract version string (e.g., "Python 3.9.6" -> "3.9.6")
    version_str = output.split()[1]
    return tuple(map(int, version_str.split(".")))


def ensure_python3_symlink() -> bool:
    """Ensure 'python' command points to Python 3."""
    # Check if 'python' command exists and points to Python 3
    python_version = get_python_version("python")
    if python_version and python_version[0] == 3:
        print("✅ 'python' command already points to Python 3")
        return True

    # Try to find Python 3 executable
    python3_path = shutil.which("python3")
    if not python3_path:
        print("❌ Python 3 not found. Please install Python 3.9 or higher.")
        return False

    # On macOS/Linux, we can create a symlink in ~/bin
    bin_dir = Path.home() / "bin"
    bin_dir.mkdir(exist_ok=True)

    python_symlink = bin_dir / "python"

    try:
        if python_symlink.exists():
            python_symlink.unlink()
        python_symlink.symlink_to(python3_path)

        # Add ~/bin to PATH if not already there
        shell_config = (
            Path.home() / ".zshrc"
            if "zsh" in os.getenv("SHELL", "")
            else Path.home() / ".bashrc"
        )

        path_addition = '\n# Add ~/bin to PATH\nexport PATH="$HOME/bin:$PATH"\n'

        if (
            not shell_config.exists()
            or path_addition.strip() not in shell_config.read_text()
        ):
            with open(shell_config, "a") as f:
                f.write(path_addition)
            print(f"✅ Added ~/bin to PATH in {shell_config}")

        print(f"✅ Created symlink: {python_symlink} -> {python3_path}")
        print("\nPlease restart your terminal or run:")
        print(f"  source {shell_config}")
        return True

    except Exception as e:
        print(f"❌ Failed to create symlink: {e}")
        print("\nManual alias: add this to your shell config:")
        print(f"  alias python='{python3_path}'")
        return False


def ensure_virtualenv() -> bool:
    """Ensure a virtual environment is set up using the project's venv_utils."""
    try:
        # Import the venv_utils module
        import sys
        from pathlib import Path
        
        # Add the project root to the path so we can import scripts.venv_utils
        project_root = Path(__file__).parent.parent
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))
            
        from scripts import venv_utils
        
        # Create the virtual environment if it doesn't exist
        if not venv_utils.get_venv_dir().exists():
            print("Creating virtual environment...")
            if not venv_utils.create_venv():
                print("❌ Failed to create virtual environment")
                return False
            print(f"✅ Created virtual environment at {venv_utils.get_venv_dir()}")
        else:
            print(f"✅ Virtual environment exists at {venv_utils.get_venv_dir()}")
        
        # Check if the virtual environment is activated
        if not venv_utils.is_project_venv_activated():
            print("⚠️  Virtual environment is not activated.")
            print(f"   Please run: source {venv_utils.get_venv_dir()}/bin/activate")
            print("   Then run this script again.")
            return False
            
        print("✅ Virtual environment is active")
        return True
        
    except ImportError as e:
        print(f"❌ Failed to import venv_utils: {e}")
        print("Make sure you're running this script from the project root.")
        return False
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        return False


def install_dependencies() -> bool:
    """Install project dependencies."""
    if not os.path.exists("pyproject.toml"):
        print("❌ pyproject.toml not found. Are you in the project root?")
        return False

    print("Installing dependencies...")
    success, output = run_command(["pip", "install", "-e", ".[dev]"])

    if not success:
        print(f"❌ Failed to install dependencies: {output}")
        return False

    print("✅ Installed project dependencies")
    return True


def main() -> None:
    """Main entry point."""
    print("=" * 60)
    print("Python Environment Setup")
    print("=" * 60)

    # Check Python version
    python3_version = get_python_version("python3")
    if not python3_version:
        print("❌ Python 3 (3.9+) is not installed. Please install it.")
        sys.exit(1)

    print(f"✅ Found Python {'.'.join(map(str, python3_version))}")

    # Ensure python command points to Python 3
    # Symlinks don't work the same way on Windows
    if platform.system() != "Windows":
        print("\nEnsuring 'python' command points to Python 3...")
        ensure_python3_symlink()

    # Set up virtual environment
    print("\nSetting up virtual environment...")
    if not ensure_virtualenv():
        sys.exit(1)

    # Install dependencies
    print("\nInstalling project dependencies...")
    if not install_dependencies():
        sys.exit(1)

    print("\n" + "=" * 60)
    print("✅ Setup complete!")
    print("\nNext steps:")
    print("1. Activate the virtual environment:")
    print("   source .venv/bin/activate  # On macOS/Linux")
    print("   .venv\\Scripts\\activate    # On Windows")
    print("2. Run the application:")
    print("   ./run_app.sh")
    print("3. Run the tests:")
    print("   ./run_tests.sh")
    print("\nFor more info, see docs in docs/ directory.")


if __name__ == "__main__":
    main()
