"""Base implementation of the Agent protocol."""

import abc
from typing import Any, Dict, Optional

from .protocols import Agent as AgentProtocol
from .protocols import AgentContext, AgentMessage, AgentRole


class Agent(AgentProtocol, abc.ABC):
    """Base class for all agents in the system.

    This class provides common functionality and implements the Agent protocol.
    Specific agent implementations should subclass this and implement the abstract
    methods.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the agent with optional configuration.

        Args:
            config: Agent-specific configuration
        """
        self._config = config or {}

    @property
    @abc.abstractmethod
    def role(self) -> AgentRole:
        """The role this agent performs in the system."""
        ...

    async def process_message(
        self, message: AgentMessage, context: AgentContext
    ) -> AgentMessage:
        """Process an incoming message and return a response.

        This base implementation adds the incoming message to the context's
        message history and delegates to _process_message for the actual
        processing.

        Args:
            message: The incoming message to process
            context: The current execution context

        Returns:
            The agent's response message
        """
        try:
            context.add_message(message)
            return await self._process_message(message, context)
        except Exception as e:
            # Create an error response
            return AgentMessage(
                role=self.role,
                content=f"Error processing message: {str(e)}",
                metadata={"status": "error", "error": str(e)},
            )

    @abc.abstractmethod
    async def _process_message(
        self, message: AgentMessage, context: AgentContext
    ) -> AgentMessage:
        """Process the incoming message and return a response.

        Subclasses must implement this method to provide their specific behavior.

        Args:
            message: The incoming message to process
            context: The current execution context

        Returns:
            The agent's response message
        """
        ...

    def __repr__(self) -> str:
        """Return a string representation of the agent."""
        return f"{self.__class__.__name__}(role={self.role})"
