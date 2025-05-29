"""CLI commands for interacting with the Architect agent."""

import typer
from typing import Optional
from rich.console import Console
from rich.panel import Panel

# Import from the full path to avoid relative import issues
from agent_core.agents.architect import ArchitectAgent
from agent_core.base import AgentContext, AgentMessage, AgentRole

# Create the Typer app
app = typer.Typer(help="Commands for the Architect agent")
console = Console()

@app.command(name="analyze")
def analyze_project(
    project_path: str = typer.Argument(
        ...,
        help="Path to the project to analyze"
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v",
        help="Enable verbose output"
    ),
):
    """Analyze the project structure and provide architectural insights."""
    try:
        agent = ArchitectAgent()
        context = AgentContext(
            project_root=project_path,
            config={"verbose": verbose}
        )
        
        console.print(Panel(
            "[bold blue]Architect Agent[/bold blue] - Analyzing project...",
            border_style="blue"
        ))
        
        # Create a message to trigger project structure analysis
        message = AgentMessage(
            role=AgentRole.ARCHITECT,
            content="Show me the project structure"
        )
        
        # Run the agent asynchronously
        import asyncio
        response = asyncio.run(agent.process_message(message, context))
        
        # Print the response
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
