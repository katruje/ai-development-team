"""Tests for the DeveloperAgent class."""

import unittest
from pathlib import Path
import tempfile
import shutil
from unittest.mock import patch

from agent_core.agents.developer.agent import DeveloperAgent
from agent_core.base import AgentContext, AgentMessage, AgentRole


class TestDeveloperAgent(unittest.IsolatedAsyncioTestCase):
    """Test cases for DeveloperAgent class."""

    async def asyncSetUp(self):
        """Set up test fixtures."""
        self.agent = DeveloperAgent()
        self.temp_dir = Path(tempfile.mkdtemp())
        # Ensure the directory exists
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        self.context = AgentContext(
            project_root=self.temp_dir, config={"test_mode": True}
        )

        # Create a test file
        self.test_file = self.temp_dir / "test_file.py"
        self.test_file.touch()

        # _process_message is no longer patched to allow testing actual agent
        # logic

    async def asyncTearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    async def test_role_property(self):
        """Test the role property returns DEVELOPER."""
        self.assertEqual(self.agent.role, AgentRole.DEVELOPER)

    async def test_help_message(self):
        """Test help message generation."""
        message = AgentMessage(role=AgentRole.DEVELOPER, content="help")

        response = await self.agent._process_message(message, self.context)
        # Get actual help message
        expected_help_message = self.agent._get_help_message()
        self.assertEqual(response.content, expected_help_message)
        self.assertIn("Available commands:", response.content)
        self.assertIn("- help: Show this help message", response.content)
        self.assertIn(
            "- analyze <requirements>: Analyze software requirements", response.content
        )
        self.assertIn(
            "- generate <task>: Generate code for the given task", response.content
        )

    async def test_unknown_command(self):
        """Test handling of unknown commands."""
        message = AgentMessage(role=AgentRole.DEVELOPER, content="some unknown command")

        response = await self.agent._process_message(message, self.context)
        self.assertEqual(
            response.content, "Unknown command. Type 'help' for available commands."
        )

    async def test_code_generation(self):
        """Test code generation functionality."""
        # Test with specific function request
        message = AgentMessage(
            role=AgentRole.DEVELOPER,
            content="generate a python function called factorial",
        )

        response = await self.agent._process_message(message, self.context)
        # Debug output
        print(f"Response content: {response.content}")
        self.assertIn(
            "Generated code for task: a python function called factorial",
            response.content,
        )
        # Check for part of the generated code
        self.assertIn("def _apythonfunction():", response.content)

        message = AgentMessage(
            role=AgentRole.DEVELOPER, content="generate something else"
        )
        response = await self.agent._process_message(message, self.context)
        self.assertIn("Generated code for task: something else", response.content)
        self.assertIn("def _somethingelse():", response.content)
        self.assertIn('"""something else"""', response.content)

    async def test_file_creation(self):
        """Test file creation functionality."""
        # Test with content
        test_content = "Hello, World!"
        filename = "test.txt"
        message = AgentMessage(
            role=AgentRole.DEVELOPER,
            content=f"create file {filename} with content: {test_content}",
        )

        print(f"\nTest file creation in: {self.temp_dir}")
        print(f"Current directory: {Path.cwd()}")

        # List directory before creation
        print("\nDirectory contents before creation:")
        for f in self.temp_dir.glob("*"):
            print(f"  - {f.name}")

        response = await self.agent._process_message(message, self.context)
        print(f"\nResponse: {response.content}")

        # Verify the file was created with correct content
        test_file = self.temp_dir / filename
        print(f"\nChecking for file: {test_file}")
        print(f"File exists: {test_file.exists()}")

        if test_file.exists():
            content = test_file.read_text(encoding="utf-8")
            print(f"File content: {content!r}")
        else:
            print("File was not created. Directory contents:")
            for f in self.temp_dir.glob("*"):
                print(f"  - {f.name}")

        self.assertIn("File created successfully", response.content)
        self.assertTrue(test_file.exists(), f"Expected file {test_file} to exist")
        self.assertEqual(test_file.read_text(encoding="utf-8").strip(), test_content)

        # Test with empty content
        empty_filename = "empty.txt"
        message = AgentMessage(
            role=AgentRole.DEVELOPER, content=f"create file {empty_filename}"
        )

        response = await self.agent._process_message(message, self.context)
        empty_file = self.temp_dir / empty_filename
        self.assertTrue(empty_file.exists(), f"Expected file {empty_file} to exist")
        self.assertEqual(empty_file.read_text(encoding="utf-8").strip(), "")

        # Test with invalid input (missing filename)
        message = AgentMessage(role=AgentRole.DEVELOPER, content="create file")
        response = await self.agent._process_message(message, self.context)
        self.assertEqual(
            response.content,
            "Error: File path not specified for 'create file' command.",
        )

    # def test_add_and_get_code_template(self):
    #     """Test adding and retrieving code templates."""
    #     template_name = "test_template"
    #     template_content = ("def hello():\n    # return 'Hello, World!'")
    #
    #     self.agent.add_code_template(template_name, template_content)
    #     retrieved = self.agent.get_code_template(template_name)
    #
    #     self.assertEqual(retrieved, template_content)
    #     self.assertIsNone(
    #         self.agent.get_code_template("non_existent")
    #     )

    # def test_log_file_operation(self):
    #     """Test logging file operations."""
    #     with patch(
    #         'agent_core.agents.developer.agent.logger'
    #     ) as mock_logger:
    #         # This test needs to be rewritten as log_file_operation was
    #         # removed.
    #         # Direct logging calls would be tested by checking mock_logger
    #         # calls.
    #         pass


class TestDeveloperAgentIntegration(unittest.IsolatedAsyncioTestCase):
    """Integration tests for DeveloperAgent with file system operations."""

    async def asyncSetUp(self):
        """Set up test fixtures."""
        self.agent = DeveloperAgent()
        self.temp_dir = Path(tempfile.mkdtemp())
        self.context = AgentContext(
            project_root=self.temp_dir, config={"test_mode": True}
        )
        self.test_file = self.temp_dir / "test_file.txt"
        self.test_file.write_text("Test content")

    async def asyncTearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    # This test will be expanded when we implement actual file operations
    async def test_file_operations(self):
        """Test file operations integration with actual file system."""
        # Test file reading
        content = self.test_file.read_text(encoding="utf-8")
        self.assertEqual(content, "Test content")
        test_content = "Test content"
        message = AgentMessage(
            role=AgentRole.DEVELOPER,
            content="create file subdir/test_file.txt with content: Test content",
        )

        # Ensure the subdirectory doesn't exist yet
        subdir = self.temp_dir / "subdir"
        if subdir.exists():
            shutil.rmtree(subdir)

        response = await self.agent._process_message(message, self.context)
        self.assertIn("File created successfully", response.content)

        # Verify the file was created in the subdirectory
        test_file = subdir / "test_file.txt"
        self.assertTrue(test_file.exists(), f"Expected file {test_file} to exist")
        self.assertEqual(test_file.read_text(encoding="utf-8").strip(), test_content)

        # Test error handling for invalid paths
        with patch("pathlib.Path.write_text") as mock_write:
            mock_write.side_effect = IOError("Test error")
            message = AgentMessage(
                role=AgentRole.DEVELOPER,
                content="create file error.txt with content: Should fail",
            )
            response = await self.agent._process_message(message, self.context)
            self.assertIn("Error creating file error.txt: Test error", response.content)


if __name__ == "__main__":
    unittest.main()
