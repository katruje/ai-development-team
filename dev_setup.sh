#!/bin/bash
# Development Environment Setup Script for AI Development Team

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print section headers
section() {
    echo -e "\n${GREEN}==>${NC} ${YELLOW}$1${NC}"
    echo "----------------------------------------------------------------"
}

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install packages with apt (for Debian/Ubuntu)
apt_install() {
    if ! command_exists apt-get; then
        return 1
    fi
    
    sudo apt-get update
    sudo apt-get install -y "$@"
}

# Function to install packages with brew (for macOS)
brew_install() {
    if ! command_exists brew; then
        return 1
    fi
    
    brew install "$@"
}

# Function to ensure Python is installed
ensure_python() {
    section "Checking Python Installation"
    
    local python_cmd="python3"
    local pip_cmd="pip3"
    local python_version
    
    # Check if Python is installed
    if ! command_exists "$python_cmd"; then
        echo -e "${RED}Python 3 is not installed.${NC}"
        
        # Try to install Python
        if command_exists apt-get; then
            echo "Installing Python 3 using apt..."
            apt_install python3 python3-pip python3-venv
        elif command_exists brew; then
            echo "Installing Python 3 using Homebrew..."
            brew install python@3.13
            echo 'export PATH="/opt/homebrew/opt/python@3.13/bin:$PATH"' >> ~/.zshrc
            source ~/.zshrc
        else
            echo -e "${RED}Could not install Python automatically. Please install Python 3.9+ manually.${NC}"
            exit 1
        fi
    fi
    
    # Check Python version
    python_version=$("$python_cmd" -c "import sys; print('.'.join(map(str, sys.version_info[:3])))")
    echo "Found Python $python_version"
    
    # Verify Python version is 3.9 or higher
    if ! "$python_cmd" -c "import sys; exit(0 if sys.version_info >= (3, 9) else 1)"; then
        echo -e "${RED}Python 3.9 or higher is required. Found Python $python_version${NC}"
        exit 1
    fi
    
    # Ensure pip is up to date
    "$python_cmd" -m pip install --upgrade pip
}

# Function to create and activate virtual environment
setup_virtualenv() {
    section "Setting Up Virtual Environment"
    
    # Use the new venv_utils.py to manage the virtual environment
    echo "Setting up virtual environment using venv_utils..."
    
    # Create the virtual environment if it doesn't exist
    if ! python3 -c "from scripts import venv_utils; venv_utils.create_venv()"; then
        echo -e "${RED}Failed to create virtual environment${NC}"
        exit 1
    fi
    
    # Check if we're in the correct virtual environment
    if ! python3 -c "from scripts import venv_utils; exit(0 if venv_utils.is_project_venv_activated() else 1)"; then
        venv_dir="$(python3 -c 'from scripts.venv_utils import get_venv_dir; print(get_venv_dir())')"
        echo -e "${YELLOW}Virtual environment is not activated.${NC}"
        echo -e "Please run: ${GREEN}source ${venv_dir}/bin/activate${NC}"
        echo -e "Then run this script again."
        exit 1
    fi
    
    echo -e "${GREEN}✓ Virtual environment is active${NC}"
    echo "Using Python from: $(which python3)"
}

# Function to install project dependencies
install_dependencies() {
    section "Installing Dependencies"
    
    # Install project in development mode
    pip install -e ".[dev]"
    
    # Install pre-commit hooks
    if command_exists pre-commit; then
        echo "Installing pre-commit hooks..."
        pre-commit install
    else
        echo -e "${YELLOW}pre-commit not found. Skipping pre-commit hooks installation.${NC}"
    fi
}

# Function to check environment
check_environment() {
    section "Verifying Environment"
    
    if [ -f "scripts/check_environment.py" ]; then
        python scripts/check_environment.py
    else
        echo -e "${YELLOW}Environment check script not found. Skipping environment verification.${NC}"
    fi
}

# Function to set up git hooks
setup_git_hooks() {
    section "Setting Up Git Hooks"
    
    if [ ! -d ".git" ]; then
        echo -e "${YELLOW}Not a git repository. Skipping git hooks setup.${NC}"
        return
    fi
    
    if command_exists pre-commit; then
        echo "Installing git hooks..."
        pre-commit install
    else
        echo -e "${YELLOW}pre-commit not found. Skipping git hooks setup.${NC}"
    fi
}

# Function to provide next steps
show_next_steps() {
    section "Setup Complete!"
    
    echo -e "${GREEN}✅ Development environment setup is complete!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Activate the virtual environment:"
    echo "   source .venv/bin/activate"
    echo "2. Run the tests to verify everything works:"
    echo "   ./run_tests.sh"
    echo "3. Start the application:"
    echo "   ./run_app.sh"
    echo ""
    echo "For more information, see the documentation in the docs/ directory."
}

# Main function
main() {
    echo -e "${GREEN}🚀 Setting up AI Development Team development environment...${NC}"
    
    # Ensure we're in the project root
    if [ ! -f "pyproject.toml" ]; then
        echo -e "${RED}Error: Please run this script from the project root directory.${NC}"
        exit 1
    fi
    
    # Run setup steps
    ensure_python
    setup_virtualenv
    install_dependencies
    setup_git_hooks
    check_environment
    show_next_steps
}

# Run the main function
main
