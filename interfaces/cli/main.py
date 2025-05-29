"""Command-line interface for the AI Development Team."""

import asyncio
import logging
import sys
from pathlib import Path
from typing import Optional, Dict, Type, List

import typer
from rich.console import Console
from rich.logging import RichHandler
from rich.prompt import Prompt
from rich.panel import Panel

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Set up logging first to ensure it's available for all imports
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)
logger = logging.getLogger("ai_development_team")

# Create the main CLI app
app = typer.Typer(help="AI Development Team CLI")
console = Console()

# Import base classes after setting up logging
from agent_core.base import Agent, AgentContext, AgentMessage, AgentRole

# Import and register subcommands after app is created to avoid circular imports
from interfaces.cli.commands.architect import register_commands as register_architect_commands

# Register architect commands
register_architect_commands(app)

# Agent registry
AGENT_REGISTRY: Dict[AgentRole, Type[Agent]] = {}

def register_agent(role: AgentRole, agent_class: Type[Agent]) -> None:
    """Register an agent class for a specific role.
    
    Args:
        role: The role of the agent
        agent_class: The agent class to register
    """
    AGENT_REGISTRY[role] = agent_class

# Import agent implementations after registry is defined
from agent_core.agents.architect import ArchitectAgent

# Register built-in agents
register_agent(AgentRole.ARCHITECT, ArchitectAgent)

def get_agent(role: AgentRole) -> Agent:
    """Get an agent instance for the given role.
    
    Args:
        role: The role of the agent to get
        
    Returns:
        An instance of the requested agent
        
    Raises:
        ValueError: If no agent is registered for the given role
    """
    agent_class = AGENT_REGISTRY.get(role)
    if not agent_class:
        raise ValueError(f"No agent registered for role: {role}")
    return agent_class()

class InteractiveSession:
    """Interactive session with an agent."""
    
    def __init__(self, agent: Agent, context: AgentContext):
        """Initialize the session.
        
        Args:
            agent: The agent to interact with
            context: The agent context
        """
        self.agent = agent
        self.context = context
    
    async def run(self):
        """Run the interactive session."""
        console.print(f"[bold green]AI Development Team - {self.agent.role.value.title()} Agent[/bold green]")
        console.print("Type 'exit' or 'quit' to end the session\n")
        
        while True:
            try:
                # Get user input
                user_input = Prompt.ask("You")
                
                # Check for exit commands
                if user_input.lower() in ("exit", "quit"):
                    break
                
                # Create and process the message
                message = AgentMessage(
                    role=self.agent.role,
                    content=user_input
                )
                
                # Get the agent's response
                response = await self.agent.process_message(message, self.context)
                console.print(f"[bold blue]Agent ({self.agent.role.value}):[/bold blue] {response.content}")
                
            except KeyboardInterrupt:
                console.print("\nGoodbye!")
                break
            except Exception as e:
                logger.exception("An error occurred:")

@app.command()
def start(
    project_path: str = typer.Argument(
        "project",
        help="Path to the project directory"
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose output"
    ),
    role: str = typer.Option(
        "architect", "--role", "-r", help="Agent role to start with"
    ),
):
    """Start the AI Development Team CLI."""
    # Configure logging level
    log_level = logging.DEBUG if verbose else logging.INFO
    logger.setLevel(log_level)
    
    # Initialize the agent system
    project_path = str(Path(project_path).absolute())
    context = AgentContext(
        project_root=project_path,
        config={"verbose": verbose}
    )
    
    try:
        # Get the requested agent
        agent_role = AgentRole(role.lower())
        agent = get_agent(agent_role)
        
        # Start the interactive session
        session = InteractiveSession(agent, context)
        asyncio.run(session.run())
        
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        console.print("\nAvailable roles:")
        for r in AgentRole:
            console.print(f"- {r.value}")

if __name__ == "__main__":
    app()
