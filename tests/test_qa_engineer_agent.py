"""Tests for the QA Engineer agent."""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from agent_core.agents.qa_engineer import QAEngineerAgent
from agent_core.base.protocols import AgentMessage, AgentRole, AgentContext

@pytest.fixture
def qa_agent():
    """Create a QA Engineer agent for testing."""
    return QAEngineerAgent(config={"test_coverage_threshold": 85.0})

@pytest.fixture
def test_context():
    """Create a test context for the agent."""
    return AgentContext(
        project_root="/test/project",
        config={},
        message_history=[]
    )

@pytest.mark.asyncio
async def test_generate_tests(qa_agent, test_context):
    """Test test generation functionality."""
    message = AgentMessage(
        role=AgentRole.QA_ENGINEER,
        content='generate_tests "src/example.py"',
        metadata={"test_type": "unit"}
    )
    
    response = await qa_agent.process_message(message, test_context)
    
    assert response.role == AgentRole.QA_ENGINEER
    assert "test_path" in response.metadata
    assert response.metadata.get("status") == "success"

@pytest.mark.asyncio
async def test_run_tests(qa_agent, test_context):
    """Test test execution functionality."""
    message = AgentMessage(
        role=AgentRole.QA_ENGINEER,
        content='run_tests "tests/test_example.py"',
        metadata={"coverage": True}
    )
    
    response = await qa_agent.process_message(message, test_context)
    
    assert response.role == AgentRole.QA_ENGINEER
    assert "results" in response.metadata
    assert "total" in response.metadata["results"]
    assert "coverage" in response.metadata["results"]

@pytest.mark.asyncio
async def test_unknown_command(qa_agent, test_context):
    """Test handling of unknown commands."""
    message = AgentMessage(
        role=AgentRole.QA_ENGINEER,
        content="unknown_command",
        metadata={}
    )
    
    response = await qa_agent.process_message(message, test_context)
    
    assert response.role == AgentRole.QA_ENGINEER
    assert response.content.startswith("Error: Unknown command:")
    assert response.metadata.get("status") == "error"

def test_coverage_threshold_config():
    """Test that the coverage threshold is correctly set from config."""
    custom_agent = QAEngineerAgent(config={"test_coverage_threshold": 90.0})
    assert custom_agent.test_coverage_threshold == 90.0

def test_default_coverage_threshold():
    """Test default coverage threshold when not specified in config."""
    agent = QAEngineerAgent()
    assert agent.test_coverage_threshold == 80.0  # Default from class

@pytest.mark.asyncio
async def test_generate_tests_error_handling(qa_agent, test_context):
    """Test error handling in test generation."""
    # Create a mock for the _process_message method that raises an exception
    async def mock_process_message(self, message, context):
        raise Exception("Test error")
    
    # Save the original method
    original_process_message = qa_agent._process_message
    
    try:
        # Replace the method with our mock
        qa_agent._process_message = mock_process_message.__get__(qa_agent)
        
        message = AgentMessage(
            role=AgentRole.QA_ENGINEER,
            content='generate_tests "invalid/path.py"',
            metadata={}
        )
        
        # This should now call our mock which raises an exception
        response = await qa_agent.process_message(message, test_context)
        
        # The base class should catch the exception and return an error message
        assert response.role == AgentRole.QA_ENGINEER
        assert "error" in response.content.lower()
    finally:
        # Restore the original method
        qa_agent._process_message = original_process_message
