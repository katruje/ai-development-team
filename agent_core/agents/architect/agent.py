"""Architect Agent implementation."""

import logging
from pathlib import Path
from typing import Any, Dict, Optional

from rich.console import Console
from rich.panel import Panel

from agent_core.base import Agent, AgentContext, AgentMessage, AgentRole

logger = logging.getLogger(__name__)
console = Console()

class ArchitectAgent(Agent):
    """Agent responsible for system architecture and design decisions.
    
    The Architect agent analyzes requirements, makes high-level design decisions,
    and defines the overall structure of the software system.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the Architect agent.
        
        Args:
            config: Optional configuration dictionary for the agent
        """
        super().__init__(config or {})
        self._project_structure = {}
    
    @property
    def role(self) -> AgentRole:
        """Return the role of this agent."""
        return AgentRole.ARCHITECT
    
    async def _process_message(self, message: AgentMessage, context: AgentContext) -> AgentMessage:
        """Process an incoming message and return a response.
        
        Args:
            message: The incoming message
            context: The current agent context
            
        Returns:
            AgentMessage: The response message
        """
        content = message.content.lower()
        
        if "hello" in content or "hi" in content:
            return self._create_response("Hello! I'm the Architect agent. I can help with system design and architecture.")
            
        elif "design" in content or "architecture" in content:
            return self._create_response("I can help design the system architecture. Please provide requirements or ask specific questions.")
            
        elif "project structure" in content:
            return await self._handle_project_structure(context)
            
        return self._create_response(
            "I'm the Architect agent. I can help with:\n"
            "- System architecture design\n"
            "- Project structure\n"
            "- Technology selection\n"
            "- Design patterns"
        )
    
    async def _handle_project_structure(self, context: AgentContext) -> AgentMessage:
        """Handle project structure related requests.
        
        Args:
            context: The current agent context
            
        Returns:
            AgentMessage: Response with project structure information
        """
        project_root = Path(context.project_root)
        
        if not project_root.exists():
            project_root.mkdir(parents=True, exist_ok=True)
            return self._create_response(f"Created project directory at {project_root}")
        
        # Analyze existing project structure
        structure = self._analyze_project_structure(project_root)
        
        # Display the structure in a nice format
        structure_text = self._format_structure(structure)
        console.print(Panel(f"[bold]Project Structure:[/bold]\n{structure_text}", 
                         title="Architect", border_style="blue"))
        
        return self._create_response("Here's the current project structure.")
    
    def _analyze_project_structure(self, path: Path, indent: int = 0) -> Dict:
        """Recursively analyze the project structure.
        
        Args:
            path: Path to analyze
            indent: Current indentation level
            
        Returns:
            Dict representing the directory structure
        """
        if not path.is_dir():
            return {}
            
        structure = {}
        try:
            for item in sorted(path.iterdir()):
                if item.is_dir() and not item.name.startswith('.'):
                    structure[item.name] = self._analyze_project_structure(item, indent + 1)
                elif item.is_file() and item.suffix in ('.py', '.md', '.toml'):
                    structure[item.name] = None
        except (PermissionError, OSError) as e:
            logger.warning(f"Could not access {path}: {e}")
            
        return structure
    
    def _format_structure(self, structure: Dict, indent: int = 0) -> str:
        """Format the directory structure as a string.
        
        Args:
            structure: The directory structure to format
            indent: Current indentation level
            
        Returns:
            Formatted string representation of the structure
        """
        lines = []
        for i, (name, contents) in enumerate(structure.items()):
            prefix = "    " * indent
            if i == len(structure) - 1:
                prefix += "└── "
                next_prefix = "    " * (indent + 1)
            else:
                prefix += "├── "
                next_prefix = "│   " + "    " * indent
                
            lines.append(f"{prefix}{name}")
            if contents:
                lines.append(self._format_structure(contents, indent + 1))
                
        return "\n".join(lines)
    
    def _create_response(self, content: str) -> AgentMessage:
        """Create a response message.
        
        Args:
            content: The response content
            
        Returns:
            AgentMessage: The response message
        """
        return AgentMessage(
            role=self.role,
            content=content
        )
