"""Core agent system for the AI Development Team.

This package contains the base classes and interfaces for creating autonomous
AI agents that can collaborate on software development tasks.
"""

from .base import Agent, AgentContext, AgentMessage, AgentRole

__version__ = "0.1.0"
__all__ = ["Agent", "AgentContext", "AgentMessage", "AgentRole"]
