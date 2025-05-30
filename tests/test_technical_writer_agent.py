"""Tests for the Technical Writer agent."""

from unittest.mock import AsyncMock, patch

import pytest

from agent_core.agents.technical_writer import TechnicalWriterAgent
from agent_core.base.protocols import AgentMessage, AgentRole, AgentContext

# Test configuration
TEST_CONFIG = {
    "doc_formats": ["markdown", "html"],
    "doc_style": "google",
    "include_examples": True,
}


# Fixtures
@pytest.fixture
def technical_writer_agent():
    """Create a TechnicalWriterAgent instance for testing."""
    return TechnicalWriterAgent(config=TEST_CONFIG)


@pytest.fixture
def test_context():
    """Create a test AgentContext."""
    return AgentContext(
        project_root="/test/project",
        config={"test_config": "value"},
        message_history=[],
    )


# Tests


class TestTechnicalWriterAgent:
    """Test cases for the TechnicalWriterAgent class."""

    def test_initialization(self, technical_writer_agent):
        """Test that the agent initializes with the correct configuration."""
        assert technical_writer_agent.doc_formats == ["markdown", "html"]
        assert technical_writer_agent.doc_style == "google"
        assert technical_writer_agent.include_examples is True

    @pytest.mark.asyncio
    async def test_role_property(self, technical_writer_agent):
        """Test that the role property returns the correct role."""
        assert technical_writer_agent.role == AgentRole.TECHNICAL_WRITER

    @pytest.mark.asyncio
    async def test_generate_documentation_success(
        self, technical_writer_agent, test_context
    ):
        """Test successful documentation generation."""
        # Mock the _process_message method
        with patch.object(
            technical_writer_agent, "_process_message", new_callable=AsyncMock
        ) as mock_process:
            mock_process.return_value = AgentMessage(
                role=AgentRole.TECHNICAL_WRITER,
                content="Docs generated: /test/project/docs",
                metadata={
                    "command": "documentation_generated",
                    "status": "success",
                    "output_dir": "/test/project/docs",
                    "format": "markdown",
                    "target": "/test/project/src/module.py",
                },
            )

            response = await technical_writer_agent.generate_documentation(
                target_path="/test/project/src/module.py",
                output_format="markdown",
                output_dir="/test/project/docs",
            )

            assert response.metadata["command"] == "documentation_generated"
            assert response.metadata["status"] == "success"
            assert response.metadata["output_dir"] == "/test/project/docs"

    @pytest.mark.asyncio
    async def test_generate_documentation_error(
        self, technical_writer_agent, test_context
    ):
        """Test error handling in documentation generation."""
        # Create a test message that will cause an error
        test_msg = AgentMessage(
            role=AgentRole.TECHNICAL_WRITER,
            content="Generate documentation with error",
            metadata={
                "command": "generate_docs",
                "data": {
                    "target_path": "/invalid/path.py",
                    "output_format": "markdown",
                },
            },
        )

        # Mock the _process_message method to raise an exception
        with patch.object(
            technical_writer_agent, "_process_message", new_callable=AsyncMock
        ) as mock_process:
            mock_process.side_effect = Exception("Test error")

            # Call the method that will handle the error
            response = await technical_writer_agent.process_message(
                test_msg, test_context
            )

            # Check that the response indicates an error
            assert response.role == AgentRole.TECHNICAL_WRITER
            assert "Test error" in response.content
            assert response.metadata.get("status") == "error"
            assert "Test error" in response.metadata.get("error", "")

    @pytest.mark.asyncio
    async def test_validate_documentation_success(
        self, technical_writer_agent, test_context
    ):
        """Test successful documentation validation."""
        with patch.object(
            technical_writer_agent, "_process_message", new_callable=AsyncMock
        ) as mock_process:
            mock_process.return_value = AgentMessage(
                role=AgentRole.TECHNICAL_WRITER,
                content="Validation done: /test/project/src",
                metadata={
                    "command": "validation_result",
                    "status": "success",
                    "warnings": ["Missing docstring in module.py"],
                    "errors": [],
                    "target": "/test/project/src",
                },
            )

            response = await technical_writer_agent.validate_documentation(
                target_path="/test/project/src"
            )

            assert response.metadata["command"] == "validation_result"
            assert response.metadata["status"] == "success"
            assert isinstance(response.metadata["warnings"], list)

    @pytest.mark.asyncio
    async def test_update_readme_success(self, technical_writer_agent, test_context):
        """Test successful README update."""
        with patch.object(
            technical_writer_agent, "_process_message", new_callable=AsyncMock
        ) as mock_process:
            mock_process.return_value = AgentMessage(
                role=AgentRole.TECHNICAL_WRITER,
                content="README updated: /test/project/README.md",
                metadata={
                    "command": "readme_updated",
                    "status": "success",
                    "readme_path": "/test/project/README.md",
                },
            )

            response = await technical_writer_agent.update_readme(
                project_root="/test/project"
            )

            assert response.metadata["command"] == "readme_updated"
            assert response.metadata["status"] == "success"
            assert "README updated successfully" in response.content

    @pytest.mark.asyncio
    async def test_unknown_command(self, technical_writer_agent, test_context):
        """Test handling of unknown commands."""
        message = AgentMessage(
            role=AgentRole.TECHNICAL_WRITER,
            content="Test unknown command",
            metadata={
                "command": "unknown_command",
                "data": {"test": "data"},
            },
        )

        response = await technical_writer_agent.process_message(message, test_context)

        assert response.metadata.get("error") is True
        assert "Unknown command" in response.content

    def test_create_error_response(self, technical_writer_agent):
        """Test the _create_error_response helper method."""
        error_message = "Test error message"
        response = technical_writer_agent._create_error_response(error_message)

        assert response.role == AgentRole.TECHNICAL_WRITER
        assert response.metadata.get("error") is True
        assert response.content == error_message
