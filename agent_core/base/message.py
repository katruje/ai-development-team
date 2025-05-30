"""Message types for agent communication."""

from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class AgentMessage:
    """A message passed between agents.
    
    Attributes:
        type: The type of the message (e.g., 'generate_tests', 'run_tests')
        data: The message payload
        sender: Optional name of the sending agent
        recipient: Optional name of the receiving agent
    """
    type: str
    data: Dict[str, Any]
    sender: Optional[str] = None
    recipient: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the message to a dictionary.
        
        Returns:
            Dict containing the message data
        """
        return {
            "type": self.type,
            "data": self.data,
            "sender": self.sender,
            "recipient": self.recipient
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AgentMessage':
        """Create a message from a dictionary.
        
        Args:
            data: Dictionary containing message data
            
        Returns:
            A new AgentMessage instance
        """
        return cls(
            type=data["type"],
            data=data["data"],
            sender=data.get("sender"),
            recipient=data.get("recipient")
        )
