"""Tests for the code generator module."""

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

from ai_development_team.core.generator import CodeArtifact, CodeGenerator


class TestCodeArtifact(unittest.TestCase):
    """Test cases for the CodeArtifact class."""

    def setUp(self):
        """Set up test fixtures."""
        self.artifact = CodeArtifact(
            name="test_module",
            content="def test(): pass\n",
            artifact_type="module"
        )
    
    def test_initialization(self):
        """Test artifact initialization."""
        self.assertEqual(self.artifact.name, "test_module")
        self.assertEqual(self.artifact.content, "def test(): pass\n")
        self.assertEqual(self.artifact.artifact_type, "module")
        self.assertEqual(self.artifact.language, "python")
        self.assertIn("created_at", self.artifact.metadata)
    
    def test_save(self):
        """Test saving artifact to disk."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = self.artifact.save(temp_dir)
            self.assertTrue(output_path.exists())
            self.assertEqual(output_path.name, "test_module.py")
            
            # Verify content
            with open(output_path, 'r') as f:
                content = f.read()
            self.assertEqual(content, "def test(): pass\n")
    
    def test_get_file_path(self):
        """Test getting file paths for different artifact types."""
        # Test module path
        self.artifact.artifact_type = "module"
        self.artifact.name = "package.module"
        self.assertEqual(
            self.artifact.get_file_path(),
            Path("package/module.py")
        )
        
        # Test test path
        self.artifact.artifact_type = "test"
        self.artifact.name = "test_module"
        self.assertEqual(
            self.artifact.get_file_path(),
            Path("tests/test_test_module.py")
        )
        
        # Test default path
        self.artifact.artifact_type = "other"
        self.artifact.name = "test"
        self.assertEqual(
            self.artifact.get_file_path(),
            Path("test.py")
        )


class TestCodeGenerator(unittest.TestCase):
    """Test cases for the CodeGenerator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.generator = CodeGenerator()
    
    def test_generate_module_basic(self):
        """Test basic module generation."""
        module = self.generator.generate_module(
            module_name="test_module",
            docstring="Test module.",
            imports=["os", "sys"],
            functions=[
                {
                    "name": "hello",
                    "params": ["name"],
                    "docstring": "Say hello to someone.",
                    "body": ["print(f'Hello, {name}!')"],
                    "return_type": "None"
                }
            ]
        )
        
        self.assertIsInstance(module, CodeArtifact)
        self.assertEqual(module.name, "test_module")
        self.assertIn("def hello(name) -> None:", module.content)
        self.assertIn("Say hello to someone.", module.content)
        self.assertIn("import os", module.content)
        self.assertIn("import sys", module.content)
    
    def test_generate_with_class(self):
        """Test module generation with a class."""
        module = self.generator.generate_module(
            module_name="test_classes",
            classes=[
                {
                    "name": "TestClass",
                    "docstring": "A test class.",
                    "methods": [
                        {
                            "name": "__init__",
                            "params": ["self"],
                            "docstring": "Initialize the test class.",
                            "body": ["self.value = 42"]
                        }
                    ]
                }
            ]
        )
        
        self.assertIn("class TestClass:", module.content)
        self.assertIn("A test class.", module.content)
    
    @patch('pathlib.Path.glob')
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data="template content")
    @patch('pathlib.Path.exists', return_value=True)
    def test_load_templates(self, mock_exists, mock_open, mock_glob):
        """Test loading templates from directory."""
        # Mock glob to return template files
        mock_glob.return_value = [
            Path("/templates/python/module.j2"),
            Path("/templates/python/class.j2")
        ]
        
        # Create a generator with a mock templates directory
        generator = CodeGenerator("/templates")
        
        # Verify templates were loaded
        self.assertEqual(len(generator._templates), 2)
        self.assertIn("python.module", generator._templates)
        self.assertIn("python.class", generator._templates)
    
    def test_generate_from_template(self):
        """Test generating code from a template."""
        # Create a generator with a mock template
        generator = CodeGenerator()
        generator._templates = {
            "test.template": "Hello, {{ name }}! This is a {{ thing }}."
        }
        
        # Generate from template
        result = generator.generate_from_template(
            template_name="test.template",
            context={"name": "World", "thing": "test"},
            name="greeting"
        )
        
        # Verify result
        self.assertEqual(result.content, "Hello, World! This is a test.")
        self.assertEqual(result.name, "greeting")
        self.assertEqual(result.metadata["template"], "test.template")


if __name__ == "__main__":
    unittest.main()
