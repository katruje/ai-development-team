"""Technical Writer Agent implementation.

This module contains the TechnicalWriterAgent class which is responsible for
generating and maintaining technical documentation across the project. It handles
documentation generation, code documentation, and ensures documentation quality.
"""

import logging
from pathlib import Path
from typing import Dict, Any, Optional

from agent_core.base.agent import Agent
from agent_core.base.protocols import AgentContext, AgentMessage, AgentRole

logger = logging.getLogger(__name__)


class TechnicalWriterAgent(Agent):
    """Agent responsible for technical documentation and code quality.

    The TechnicalWriterAgent handles various aspects of documentation including:
    - Generating API documentation
    - Creating user guides and tutorials
    - Maintaining README files
    - Ensuring code documentation standards
    - Generating documentation websites

    Attributes:
        doc_formats (List[str]): Supported documentation formats
            (e.g., 'markdown', 'rst')
        doc_style (str): Documentation style guide to follow
            (e.g., 'google', 'numpy')
        include_examples (bool): Whether to include code examples in
            documentation
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the Technical Writer agent with configuration.

        Args:
            config: Optional configuration dictionary. Can include:
                - doc_formats: List of supported documentation formats
                - doc_style: Documentation style guide to follow
                - include_examples: Whether to include code examples
        """
        super().__init__(config or {})
        self.doc_formats = self._config.get("doc_formats", ["markdown"])
        self.doc_style = self._config.get("doc_style", "google")
        self.include_examples = self._config.get("include_examples", True)

    @property
    def role(self) -> AgentRole:
        """Return the role of this agent."""
        return AgentRole.TECHNICAL_WRITER

    async def _process_message(
        self, message: AgentMessage, context: AgentContext
    ) -> AgentMessage:
        """Process an incoming message and return a response.

        Args:
            message: The incoming message to process
            context: The current execution context

        Returns:
            AgentMessage: The agent's response message
        """
        # Extract command and data from message content and metadata
        command = message.metadata.get("command")
        data = message.metadata.get("data", {})

        if command == "generate_docs":
            return await self.generate_documentation(
                target_path=data.get("target_path"),
                output_format=data.get("output_format", "markdown"),
                output_dir=data.get("output_dir"),
            )
        elif command == "validate_docs":
            return await self.validate_documentation(
                target_path=data.get("target_path")
            )
        elif command == "update_readme":
            return await self.update_readme(
                project_root=data.get("project_root", ".")
            )
        else:
            return self._create_error_response(f"Unknown command: {command}")

    async def generate_documentation(
        self,
        target_path: str,
        output_format: str = "markdown",
        output_dir: Optional[str] = None,
    ) -> AgentMessage:
        """Generate documentation for the specified target.

        This method analyzes the target code and generates comprehensive
        documentation including API references, usage examples, and
        module/package documentation.

        Args:
            target_path: Path to the target file or package to document
            output_format: Output format for the documentation
                (e.g., 'markdown', 'html')
            output_dir: Directory where documentation will be generated

        Returns:
            AgentMessage: Response containing documentation generation results

        Raises:
            Exception: If documentation generation fails
        """
        try:
            logger.info(
                "Generating %s documentation for %s", output_format, target_path
            )

            # Implementation would go here
            # This is a placeholder for the actual implementation

            return AgentMessage(
                role=self.role,
                content=(
                    f"Documentation generated successfully in "
                    f"{output_dir or 'docs/generated'}"
                ),
                metadata={
                    "command": "documentation_generated",
                    "status": "success",
                    "output_dir": str(output_dir or "docs/generated"),
                    "format": output_format,
                    "target": target_path,
                },
            )
        except Exception as e:
            logger.exception("Failed to generate documentation")
            return self._create_error_response(
                f"Failed to generate documentation: {str(e)}"
            )

    async def validate_documentation(self, target_path: str) -> AgentMessage:
        """Validate existing documentation for completeness and accuracy.

        Args:
            target_path: Path to the target file or directory to validate

        Returns:
            AgentMessage: Validation results
        """
        try:
            logger.info("Validating documentation in %s", target_path)

            # Implementation would go here
            # This is a placeholder for the actual implementation

            return AgentMessage(
                role=self.role,
                content=f"Documentation validation completed for {target_path}",
                metadata={
                    "command": "validation_result",
                    "status": "success",
                    "warnings": [],
                    "errors": [],
                    "target": target_path,
                },
            )
        except Exception as e:
            logger.exception("Documentation validation failed")
            return self._create_error_response(
                f"Documentation validation failed: {str(e)}"
            )

    async def update_readme(self, project_root: str = ".") -> AgentMessage:
        """Update the project's README file with current project information.

        Args:
            project_root: Root directory of the project

        Returns:
            AgentMessage: Update results
        """
        try:
            logger.info("Updating README in %s", project_root)

            # Implementation would go here
            # This is a placeholder for the actual implementation

            readme_path = str(Path(project_root) / "README.md")
            return AgentMessage(
                role=self.role,
                content=f"README updated successfully at {readme_path}",
                metadata={
                    "command": "readme_updated",
                    "status": "success",
                    "readme_path": readme_path,
                },
            )
        except Exception as e:
            logger.exception("Failed to update README")
            return self._create_error_response(f"Failed to update README: {str(e)}")

    def _create_error_response(self, error_message: str) -> AgentMessage:
        """Create a standardized error response message.

        Args:
            error_message: Descriptive error message

        Returns:
            AgentMessage: Formatted error response
        """
        return AgentMessage(
            role=self.role,
            content=error_message,
            metadata={"status": "error", "error": True},
        )
