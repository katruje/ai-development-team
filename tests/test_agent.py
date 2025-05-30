"""Tests for the DeveloperAgent class."""

import unittest
from pathlib import Path

from agent_core.agents.developer.agent import DeveloperAgent
from agent_core.base import AgentContext, AgentRole


class TestDeveloperAgent(unittest.TestCase):
    """Test cases for the DeveloperAgent class."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary directory for the test project
        self.temp_dir = Path(__file__).parent / "temp_test_project"
        self.temp_dir.mkdir(exist_ok=True)

        # Initialize the agent and context with required arguments
        self.agent = DeveloperAgent(
            config={"name": "TestAgent", "role": "tester"},
        )
        self.test_context = AgentContext(
            project_root=self.temp_dir,
            config={"test": True},
        )

    def tearDown(self):
        """Clean up after tests."""
        # Clean up the temporary directory
        if self.temp_dir.exists():
            import shutil

            shutil.rmtree(self.temp_dir)

    def test_initialization(self):
        """Test agent initialization with default values."""
        self.assertEqual(self.agent.name, "TestAgent")
        self.assertEqual(self.agent.role, AgentRole.DEVELOPER)
        self.assertIn("python", self.agent.skills)
        self.assertIn("conversation", self.agent.memory)
        self.assertIn("tasks", self.agent.memory)

    def test_analyze_requirements(self):
        """Test requirements analysis."""
        requirements = "Create a function that calculates factorials"
        result = self.agent.analyze_requirements(requirements)

        self.assertIn("user_stories", result)
        self.assertIn("acceptance_criteria", result)
        self.assertIn("technical_requirements", result)
        self.assertIn("open_questions", result)
        self.assertEqual(
            self.agent.memory["initial_requirements"],
            requirements,
        )
        self.assertIn(
            "analyzed_requirements",
            self.agent.memory,
        )

    def test_generate_code(self):
        """Test code generation."""
        task = "Create a test function"
        code, metadata = self.agent.generate_code(task)

        self.assertIn("def test_", code)
        self.assertEqual(metadata["language"], "python")
        self.assertIn("1", self.agent.memory["tasks"])
        self.assertEqual(self.agent.memory["tasks"]["1"]["description"], task)

    def test_write_code(self):
        """Test the write_code method."""
        test_file = self.temp_dir / "test_file.py"
        test_code = "def main(): pass"

        # Test writing new file
        result = self.agent.write_code(str(test_file), test_code)
        self.assertTrue(result)
        self.assertTrue(test_file.exists())
        self.assertEqual(test_file.read_text(), test_code)

        # Test overwrite protection
        with self.assertRaises(FileExistsError):
            self.agent.write_code(str(test_file), "new code")

        # Test forced overwrite
        result = self.agent.write_code(str(test_file), "new code", overwrite=True)
        self.assertTrue(result)
        self.assertEqual(test_file.read_text(), "new code")

    def test_review_code(self):
        """Test code review functionality."""
        code = "def test(): pass"
        review = self.agent.review_code(code)

        self.assertIn("status", review)
        self.assertIn("feedback", review)
        self.assertIn("suggestions", review)
        self.assertEqual(review["status"], "reviewed")

    def test_update_knowledge(self):
        """Test updating the knowledge base."""
        new_knowledge = {"design_patterns": ["singleton", "observer"]}
        self.agent.update_knowledge(new_knowledge)

        self.assertIn("design_patterns", self.agent.knowledge_base)
        self.assertEqual(len(self.agent.knowledge_base["design_patterns"]), 2)

    def test_memory_isolation(self):
        """Test that different agents have isolated memory."""
        agent2 = DeveloperAgent(name="AnotherAgent", role="developer")
        self.agent.memory["test"] = "value"

        self.assertNotIn("test", agent2.memory)
        self.assertNotEqual(id(self.agent.memory), id(agent2.memory))


if __name__ == "__main__":
    unittest.main()
