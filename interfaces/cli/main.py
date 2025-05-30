"""Command-line interface for the AI Development Team."""

import asyncio
import logging
import sys
from enum import Enum
from pathlib import Path
from typing import Optional, Dict, Type, List, Any, TypeVar, Generic

import typer
from rich.console import Console
from rich.logging import RichHandler
from rich.prompt import Prompt
from rich.panel import Panel

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)
logger = logging.getLogger("ai_development_team")

# Create the main Typer app
app = typer.Typer(
    name="ai-dev-team",
    help="AI Development Team CLI",
    add_completion=False,
)

# Import agent core components
try:
    from agent_core.agents.architect.agent import ArchitectAgent
    from agent_core.base.agent import AgentRole, Agent
    from agent_core.base.protocols import AgentContext
except ImportError as e:
    logging.error("Failed to import agent core components: %s", e)
    raise

# Import commands
from .commands.architect import register_commands as register_architect_commands
from .commands.qa import app as qa_app
from .commands.technical_writer import app as docs_app

# Register commands from modules
app.add_typer(qa_app, name="qa", help="QA Engineer commands")
app.add_typer(docs_app, name="docs", help="Documentation and technical writing commands")
register_architect_commands(app)

# Agent registry
agent_registry: Dict[AgentRole, Type[Agent]] = {}

def register_agent(role: AgentRole, agent_class: Type[Agent]) -> None:
    """Register an agent class for a specific role.
    
    Args:
        role: The role of the agent
        agent_class: The agent class to register
    """
    agent_registry[role] = agent_class
    logger.debug("Registered agent %s for role %s", agent_class.__name__, role)

# Import agent implementations after registry is defined
from agent_core.agents.architect import ArchitectAgent
# DevelopmentAgent is now imported from agent_core.agents.architect.agent
from agent_core.agents.architect.agent import ArchitectAgent as DevelopmentAgent

# Register built-in agents
register_agent(AgentRole.ARCHITECT, ArchitectAgent)
register_agent(AgentRole.DEVELOPER, DevelopmentAgent)

def get_agent(role: AgentRole) -> Agent:
    """Get an agent instance for the given role.
    
    Args:
        role: The role of the agent to get
        
    Returns:
        An instance of the requested agent
        
    Raises:
        ValueError: If no agent is registered for the given role
    """
    if role not in agent_registry:
        raise ValueError(f"No agent registered for role: {role}")
    
    agent_class = agent_registry[role]
    logger.debug("Creating agent instance for role %s: %s", role, agent_class.__name__)
    return agent_class()

class InteractiveSession:
    """Interactive session with an agent."""
    
    def __init__(self, agent: Agent, context: AgentContext) -> None:
        """Initialize the session.
        
        Args:
            agent: The agent to interact with
            context: The agent context
        """
        self.agent = agent
        self.context = context
        self.console = Console()
    
    async def run(self) -> None:
        """Run the interactive session."""
        self.console.print(Panel.fit(
            f"[bold blue]AI Development Team - {self.agent.role.value} Session[/bold blue]\n"
            f"Type 'exit' to end the session.",
            border_style="blue"
        ))
        
        while True:
            try:
                user_input = Prompt.ask("\n[bold]You[/bold]")
                
                if user_input.lower() in ("exit", "quit"):
                    self.console.print("\n[bold]Ending session. Goodbye![/bold]")
                    break
                
                # Process the input with the agent
                response = await self.agent.process_input(user_input, self.context)
                self.console.print(f"\n[bold]{self.agent.role.value}:[/bold] {response}")
                
            except KeyboardInterrupt:
                self.console.print("\n[bold]Interrupted by user.[/bold]")
                break
            except Exception as e:  # pylint: disable=broad-except
                self.console.print(f"\n[bold red]Error: {e}[/bold red]")
                logger.exception("Error in interactive session")

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
) -> None:
    """Start the AI Development Team CLI."""
    # Set logging level
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.getLogger().setLevel(log_level)
    
    # Resolve project path
    project_path = Path(project_path).resolve()
    
    # Create project directory if it doesn't exist
    project_path.mkdir(parents=True, exist_ok=True)
    
    # Create agent context
    context = AgentContext(
        project_path=project_path,
        verbose=verbose
    )
    
    # Get the agent
    try:
        agent_role = AgentRole(role.upper())
        agent = get_agent(agent_role)
    except ValueError as e:
        logger.error("Invalid agent role: %s", role)
        logger.info("Available roles: %s", ", ".join(r.value.lower() for r in AgentRole))
        raise typer.Exit(1) from e
    
    # Start interactive session
    console = Console()
    console.print(f"[bold green]Starting {agent_role.value} session...[/bold green]")
    
    session = InteractiveSession(agent, context)
    asyncio.run(session.run())

if __name__ == "__main__":
    app()
