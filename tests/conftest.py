"""Test configuration and fixtures."""

import pytest
from ai_development_team.core.agent import DevelopmentAgent


@pytest.fixture
def sample_agent():
    """Create a sample DevelopmentAgent instance for testing."""
    return DevelopmentAgent(
        name="TestAgent",
        role="tester",
        skills=["python", "testing"],
        knowledge_base={"test_knowledge": True}
    )


@pytest.fixture
def sample_requirements():
    """Return sample requirements for testing."""
    return "Create a function that calculates factorials"


@pytest.fixture
def sample_code():
    """Return sample code for testing."""
    return """
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n-1)
"""
