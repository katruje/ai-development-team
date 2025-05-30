"""Core protocols and types for the agent system."""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Protocol, runtime_checkable


class AgentRole(str, Enum):
    """Roles that agents can take within the system."""

    ARCHITECT = "architect"
    DEVELOPER = "developer"
    QA_ENGINEER = "qa_engineer"
    TECHNICAL_WRITER = "technical_writer"


@dataclass
class AgentMessage:
    """A message passed between agents or from the system to an agent."""

    role: AgentRole
    content: str
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@runtime_checkable
class Agent(Protocol):
    """Protocol that all agents must implement."""

    @property
    def role(self) -> AgentRole:
        """The role this agent performs in the system."""
        ...

    async def process_message(
        self, message: AgentMessage, context: "AgentContext"
    ) -> AgentMessage:
        """Process an incoming message and return a response.

        Args:
            message: The incoming message to process
            context: The current execution context

        Returns:
            The agent's response message
        """
        ...


@dataclass
class AgentContext:
    """Context passed to agents during message processing."""

    project_root: str
    """Root directory of the current project."""

    config: Dict[str, Any]
    """Configuration for the current execution."""

    message_history: List[AgentMessage] = None
    """History of messages in the current conversation."""

    def __post_init__(self):
        if self.message_history is None:
            self.message_history = []

    def add_message(self, message: AgentMessage) -> None:
        """Add a message to the history."""
        self.message_history.append(message)
