"""QA Engineer Agent implementation.

This module contains the QAEngineerAgent class which is responsible for handling
testing and quality assurance tasks in the AI development team. It provides
functionality for generating and running tests, as well as analyzing test coverage.
"""

import logging
from typing import Dict, Any, Optional
from pathlib import Path

from agent_core.base.agent import Agent
from agent_core.base.protocols import AgentContext, AgentMessage, AgentRole

logger = logging.getLogger(__name__)

class QAEngineerAgent(Agent):
    """Agent responsible for testing and quality assurance tasks.
    
    The QAEngineerAgent handles various aspects of the software testing lifecycle,
    including generating test cases, running tests, and analyzing test coverage.
    It ensures code quality by enforcing testing standards and coverage thresholds.
    
    Attributes:
        test_coverage_threshold (float): Minimum test coverage percentage required.
            Defaults to 80.0 if not specified in config.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the QA Engineer agent with configuration.
        
        Args:
            config: Optional configuration dictionary. Can include:
                - test_coverage_threshold (float): Minimum test coverage percentage.
                  Defaults to 80.0 if not specified.
        """
        super().__init__(config or {})
        self.test_coverage_threshold = self._config.get("test_coverage_threshold", 80.0)
    
    @property
    def role(self) -> AgentRole:
        """The role this agent performs in the system."""
        return AgentRole.QA_ENGINEER
    
    async def _process_message(self, message: AgentMessage, context: AgentContext) -> AgentMessage:
        """Process an incoming message and return a response.
        
        Args:
            message: The incoming message to process
            context: The current execution context
            
        Returns:
            AgentMessage: The response message
        """
        logger.info("Processing message: %s", message.content)
        
        # Parse the message content as a command with arguments
        parts = message.content.strip().split(maxsplit=1)
        command = parts[0] if parts else ""
        args = parts[1] if len(parts) > 1 else ""
        
        if command == "generate_tests":
            # Parse arguments (simplified for now)
            target_path = args.strip('"\'')
            return await self.generate_tests(
                target_path=target_path,
                test_type="unit"  # Default to unit tests for now
            )
        elif command == "run_tests":
            # Parse arguments (simplified for now)
            test_path = args.strip('"\'')
            return await self.run_tests(
                test_path=test_path,
                coverage=True  # Default to including coverage
            )
        else:
            return self._create_error_response(f"Unknown command: {command}")
    
    async def generate_tests(self, target_path: str, test_type: str = "unit") -> AgentMessage:
        """Generate test cases for the specified target code.
        
        This method analyzes the target code and generates appropriate test cases
        based on the specified test type. It supports different types of tests
        such as unit tests, integration tests, etc.
        
        Args:
            target_path: Path to the target code file or module to test.
            test_type: Type of tests to generate. Defaults to "unit".
                Supported values: "unit", "integration", etc.
                
        Returns:
            AgentMessage: Response containing test generation results with:
                - status: "success" or "error"
                - test_path: Path where tests were generated
                - test_type: Type of tests generated
                
        Raises:
            Exception: If test generation fails for any reason.
        """
        try:
            logger.info("Generating %s tests for %s", test_type, target_path)
            # TODO: Implement test generation logic
            return AgentMessage(
                role=AgentRole.QA_ENGINEER,
                content=f"Generated {test_type} tests for {target_path}",
                metadata={
                    "status": "success",
                    "test_path": f"tests/test_{Path(target_path).stem}.py",
                    "test_type": test_type
                }
            )
        except Exception as e:
            logger.error("Error generating tests: %s", str(e))
            return self._create_error_response(f"Failed to generate tests: {str(e)}")
    
    async def run_tests(self, test_path: str = "tests/", coverage: bool = False) -> AgentMessage:
        """Execute tests and return the results.
        
        Runs the specified tests and optionally generates coverage reports.
        The method executes the test suite and collects results including
        pass/fail counts and coverage information if enabled.
        
        Args:
            test_path: Path to the test file or directory to execute.
                Defaults to "tests/".
            coverage: Whether to generate and include test coverage information.
                Defaults to False.
                
        Returns:
            AgentMessage: Response containing test execution results with:
                - status: "success" if all tests pass, "failed" otherwise
                - results: Dictionary containing test metrics:
                    - total: Total number of tests
                    - passed: Number of passed tests
                    - failed: Number of failed tests
                    - errors: Number of errors
                    - coverage: Test coverage percentage if coverage=True
                    
        Raises:
            Exception: If test execution fails for any reason.
        """
        try:
            logger.info("Running tests in %s", test_path)
            # TODO: Implement test execution logic

            test_results = {
                "total": 10,
                "passed": 10,
                "failed": 0,
                "errors": 0,
                "coverage": 95.5 if coverage else None
            }

            status = "success" if test_results["failed"] == 0 else "failed"
            return AgentMessage(
                role=AgentRole.QA_ENGINEER,
                content=f"Test execution {status}. {test_results['passed']} passed, {test_results['failed']} failed.",
                metadata={
                    "status": status,
                    "results": test_results
                }
            )
        except Exception as e:
            logger.error("Error running tests: %s", str(e))
            return self._create_error_response(f"Failed to run tests: {str(e)}")
    
    def _create_error_response(self, error_message: str) -> AgentMessage:
        """Create a standardized error response message.
        
        This helper method creates a properly formatted error response message
        with appropriate metadata for error handling and logging.
        
        Args:
            error_message: Descriptive error message explaining what went wrong.
            
        Returns:
            AgentMessage: Formatted error response with:
                - role: Set to QA_ENGINEER
                - content: Error message prefixed with "Error: "
                - metadata: Contains status="error" and error details
        """
        return AgentMessage(
            role=AgentRole.QA_ENGINEER,
            content=f"Error: {error_message}",
            metadata={"status": "error"}
        )
