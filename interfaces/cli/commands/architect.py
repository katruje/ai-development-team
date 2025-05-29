"""CLI commands for interacting with the Architect agent."""

import asyncio
import typer
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.panel import Panel

from agent_core.agents.architect import ArchitectAgent
from agent_core.base import AgentContext, AgentMessage, AgentRole

# Create the Typer app for architect commands
app = typer.Typer(help="Architect agent commands")
console = Console()

def register_commands(main_app: typer.Typer) -> None:
    """Register architect commands with the main app.
    
    Args:
        main_app: The main Typer app to register commands with
    """
    main_app.add_typer(
        app,
        name="architect",
        help="Architect agent commands"
    )

def create_agent_context(project_path: str, verbose: bool = False) -> AgentContext:
    """Create an agent context with the given project path."""
    return AgentContext(
        project_root=str(Path(project_path).absolute()),
        config={
            "verbose": verbose,
            "project_path": str(Path(project_path).absolute())
        }
    )

@app.command("analyze")
def analyze_project(
    project_path: str = typer.Argument(
        "",
        help="Path to the project directory (default: current directory)",
        show_default=True
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v",
        help="Enable verbose output"
    ),
):
    """Analyze a project's structure and dependencies."""
    try:
        project_path = project_path or "."
        context = create_agent_context(project_path, verbose)
        
        if verbose:
            console.print(f"[dim]Analyzing project at: {context.project_root}[/]")
        
        agent = ArchitectAgent()
        
        # Run analysis
        message = AgentMessage(
            role=AgentRole.ARCHITECT,
            content="analyze project"
        )
        
        response = asyncio.run(agent.process_message(message, context))
        
        if response and response.content:
            console.print(f"\n{response.content}")
            
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}", style="bold red")
        if verbose:
            import traceback
            console.print(traceback.format_exc())
        raise typer.Exit(1)

@app.command("structure")
def show_structure(
    project_path: str = typer.Argument(
        "",
        help="Path to the project directory (default: current directory)",
        show_default=True
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v",
        help="Enable verbose output"
    ),
):
    """Show the project's file structure."""
    try:
        project_path = project_path or "."
        context = create_agent_context(project_path, verbose)
        
        if verbose:
            console.print(f"[dim]Showing structure for: {context.project_root}[/]")
        
        agent = ArchitectAgent()
        
        # Request project structure
        message = AgentMessage(
            role=AgentRole.ARCHITECT,
            content="show project structure"
        )
        
        response = asyncio.run(agent.process_message(message, context))
        
        if response and response.content:
            console.print(f"\n{response.content}")
            
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}", style="bold red")
        if verbose:
            import traceback
            console.print(traceback.format_exc())
        raise typer.Exit(1)

@app.command(name="design")
def design_system(
    requirements: str = typer.Argument(
        ...,
        help="Requirements to design a solution for"
    ),
    output_file: Optional[str] = typer.Option(
        None, "--output", "-o",
        help="Output file for the design document"
    ),
):
    """Generate a system design based on the given requirements."""
    console.print(Panel(
        "[bold blue]Architect Agent[/bold blue] - Generating design...",
        border_style="blue"
    ))
    
    console.print(f"[bold]Designing solution for:[/bold] {requirements}")
    if output_file:
        console.print(f"[dim]Output will be saved to: {output_file}[/dim]")
    
    # TODO: Implement design generation
    console.print("[yellow]Design generation is not yet implemented.[/yellow]")
    console.print("\nThis command will generate a system design based on the provided requirements.")

# This allows the module to be run directly for testing
if __name__ == "__main__":
    app()
