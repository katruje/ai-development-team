"""Base agent abstractions and interfaces.

This module contains the foundational classes and protocols for all agents
in the AI development team.
"""

from .agent import Agent
from .protocols import AgentContext, AgentMessage, AgentRole

__all__ = ["Agent", "AgentContext", "AgentMessage", "AgentRole"]
