"""Tests for the ArchitectAgent class."""

import unittest
from unittest.mock import patch, MagicMock, AsyncMock
from pathlib import Path
import tempfile
import shutil
from io import StringIO

from agent_core.agents.architect.agent import ArchitectAgent, ProjectAnalyzer
from agent_core.base import AgentContext, AgentMessage, AgentRole


class TestArchitectAgent(unittest.IsolatedAsyncioTestCase):
    """Test cases for the ArchitectAgent class."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary directory for the test project
        self.temp_dir = Path(tempfile.mkdtemp())
        (self.temp_dir / "src").mkdir()
        (self.temp_dir / "tests").mkdir()
        
        # Create a sample Python file
        (self.temp_dir / "src" / "example.py").write_text("def hello():\n    return 'Hello, World!'\n")
        
        # Initialize the agent and context
        self.agent = ArchitectAgent(config={"test": True})
        self.context = AgentContext(
            project_root=str(self.temp_dir),
            config={"test": True}
        )
    
    def tearDown(self):
        """Clean up after tests."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    async def test_role_property(self):
        """Test the role property returns the correct role."""
        self.assertEqual(self.agent.role, AgentRole.ARCHITECT)
    
    async def test_handle_project_structure(self):
        """Test handling project structure requests."""
        message = AgentMessage(
            role=AgentRole.ARCHITECT,
            content="Show me the project structure"
        )
        
        # Capture the output of the print statements
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            response = await self.agent._process_message(message, self.context)
            output = mock_stdout.getvalue()
        
        self.assertIn("Project Structure", response.content)
        self.assertIn("example.py", output)
    
    async def test_analyze_project(self):
        """Test project analysis."""
        message = AgentMessage(
            role=AgentRole.ARCHITECT,
            content="Analyze the project"
        )
        
        response = await self.agent._process_message(message, self.context)
        self.assertIn("Project Analysis", response.content)
        self.assertIn("Python Files", response.content)
        self.assertIn("Dependencies", response.content)
    
    async def test_help_message(self):
        """Test the help message response."""
        message = AgentMessage(
            role=AgentRole.ARCHITECT,
            content="help"
        )
        
        response = await self.agent._process_message(message, self.context)
        self.assertIn("Architect Agent Help", response.content)
        self.assertIn("Available commands", response.content)
    
    async def test_unknown_command(self):
        """Test handling of unknown commands."""
        message = AgentMessage(
            role=AgentRole.ARCHITECT,
            content="some unknown command"
        )
        
        response = await self.agent._process_message(message, self.context)
        self.assertIn("I'm the Architect agent", response.content)
        self.assertIn("analyze the project", response.content)


class TestProjectAnalyzer(unittest.TestCase):
    """Test cases for the ProjectAnalyzer class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())
        (self.temp_dir / "src").mkdir()
        (self.temp_dir / "tests").mkdir()
        
        # Create sample files
        (self.temp_dir / "src" / "module1.py").write_text("import os\n\ndef func1():\n    return 'Hello'")
        (self.temp_dir / "requirements.txt").write_text("requests>=2.25.0\npytest\n")
        
        self.analyzer = ProjectAnalyzer(self.temp_dir)
    
    def tearDown(self):
        """Clean up after tests."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_analyze(self):
        """Test project analysis."""
        self.analyzer.analyze()
        analysis = self.analyzer.get_analysis()
        
        # Check if python_files is an integer (count of files)
        self.assertIsInstance(analysis['python_files'], int)
        self.assertGreaterEqual(analysis['python_files'], 1)
        
        # Check if imports is a list and contains 'os'
        self.assertIsInstance(analysis['imports'], list)
        self.assertIn('os', analysis['imports'])
        
        # Check if dependencies is a dict and contains 'requests'
        self.assertIsInstance(analysis['dependencies'], dict)
        self.assertIn('requests', analysis['dependencies'])
        self.assertEqual(analysis['dependencies']['requests'], 'requirements.txt')
    
    def test_project_structure(self):
        """Test project structure generation."""
        self.analyzer.analyze()
        structure = self.analyzer._get_project_structure()
        
        # Check if the structure contains the expected directories and files
        self.assertTrue(any(item['name'] == 'src' for item in structure))
        self.assertTrue(any(item['name'] == 'requirements.txt' for item in structure))


if __name__ == "__main__":
    unittest.main()
