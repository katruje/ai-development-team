"""Tests for the DevelopmentAgent class."""

import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime

from ai_development_team.core.agent import DevelopmentAgent


class TestDevelopmentAgent(unittest.TestCase):
    """Test cases for the DevelopmentAgent class."""

    def setUp(self):
        """Set up test fixtures."""
        self.agent = DevelopmentAgent(name="TestAgent", role="tester")

    def test_initialization(self):
        """Test agent initialization with default values."""
        self.assertEqual(self.agent.name, "TestAgent")
        self.assertEqual(self.agent.role, "tester")
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
        self.assertEqual(self.agent.memory["initial_requirements"], requirements)
        self.assertIn("analyzed_requirements", self.agent.memory)

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
        task = "Create a main function"
        with patch.object(self.agent, 'generate_code') as mock_generate:
            mock_generate.return_value = ("def main(): pass", {})
            result = self.agent.write_code(task)
            
            self.assertEqual(result, "def main(): pass")
            mock_generate.assert_called_once_with(task, None)

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
        agent2 = DevelopmentAgent(name="AnotherAgent", role="developer")
        self.agent.memory["test"] = "value"
        
        self.assertNotIn("test", agent2.memory)
        self.assertNotEqual(id(self.agent.memory), id(agent2.memory))


if __name__ == "__main__":
    unittest.main()
