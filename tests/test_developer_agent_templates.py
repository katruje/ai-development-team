"""Tests for the DeveloperAgent template functionality.

This module contains tests for the template-related functionality of the
DeveloperAgent class, ensuring that code generation and template processing
work as expected.
"""

import pytest

from agent_core.agents.developer.agent import DeveloperAgent
from agent_core.base import AgentContext


class TestDeveloperAgentTemplates:
    """Test cases for DeveloperAgent template functionality."""

    @pytest.fixture
    def agent(self):
        """Create a DeveloperAgent instance for testing."""
        return DeveloperAgent()

    @pytest.fixture
    def temp_dir(self, tmp_path):
        """Create a temporary directory for test files."""
        return tmp_path / "test_project"

    @pytest.fixture
    def context(self, temp_dir):
        """Create an AgentContext for testing."""
        return AgentContext(project_root=temp_dir, config={"test_mode": True})

    def test_check_environment(self, agent):
        """Test the check_environment method."""
        result = agent.check_environment()

        # Check basic structure
        assert "python_version" in result
        assert "virtual_env" in result
        assert "venv_path" in result
        assert "dependencies" in result
        assert "issues" in result

        # Check that required packages are in dependencies
        assert "jinja2" in result["dependencies"]

        # Check that environment_checked is updated in memory
        assert agent.memory["environment_checked"] is True
        assert "environment_status" in agent.memory

    def test_help_message_includes_template_commands(self, agent):
        """Test that help message includes template-related commands."""
        help_msg = agent._get_help_message()
        assert "generate-from-template" in help_msg
        assert "check-env" in help_msg
