"""Tests for the environment module.

This module contains tests for the environment configuration and management
functionality used throughout the application.
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agent_core.environment import Environment  # noqa: E402


def test_environment_initialization():
    """Test environment initialization."""
    env = Environment()
    assert env is not None
    assert hasattr(env, "config")
    assert isinstance(env.config, dict)


def test_environment_config_loading():
    """Test loading configuration from file."""
    # Create a temporary config file
    config_content = """
    {
        "api_key": "test_key",
        "environment": "test"
    }
    """
    mock_file = MagicMock()
    mock_file.__enter__.return_value.read.return_value = config_content

    with patch("builtins.open", return_value=mock_file) as mock_open:
        env = Environment(config_file="test_config.json")
        mock_open.assert_called_once_with("test_config.json", "r", encoding="utf-8")
        assert env.config["api_key"] == "test_key"
        assert env.config["environment"] == "test"


def test_environment_missing_config_file():
    """Test handling of missing config file."""
    with patch("builtins.open", side_effect=FileNotFoundError):
        env = Environment(config_file="nonexistent.json")
        assert env.config == {}


def test_environment_invalid_config():
    """Test handling of invalid config file."""
    mock_file = MagicMock()
    mock_file.__enter__.return_value.read.return_value = "{invalid json"

    with patch("builtins.open", return_value=mock_file):
        env = Environment(config_file="invalid.json")
        assert env.config == {}


def test_environment_get_set():
    """Test getting and setting environment values."""
    env = Environment()
    env.set("test_key", "test_value")
    assert env.get("test_key") == "test_value"
    assert env.get("nonexistent", "default") == "default"


def test_environment_required_key():
    """Test getting required keys."""
    env = Environment()
    env.set("required_key", "value")
    assert env.require("required_key") == "value"

    with pytest.raises(KeyError):
        env.require("nonexistent_key")


def test_environment_as_context_manager():
    """Test environment as a context manager."""
    with Environment() as env:
        env.set("test", "value")
        assert env.get("test") == "value"


def test_python_version():
    """Test that the Python version meets requirements."""
    assert sys.version_info >= (3, 8), "Python 3.8 or higher is required"
