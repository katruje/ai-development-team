"""CLI commands for interacting with the Architect agent."""

import asyncio
import typer
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.panel import Panel

import os
import sys

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from agent_core.agents.architect.agent import ArchitectAgent
from agent_core.base import AgentContext, AgentMessage, AgentRole
from agent_core.agents.architect.agent import ArchitectAgent as DevelopmentAgent  # Temporary alias

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
    project_name: str = typer.Option(
        ..., 
        "--project-name", "-n", 
        help="Name of the project to be generated."
    ),
    prd_content: Optional[str] = typer.Option(
        None, 
        "--prd-content", 
        help="Direct PRD content as a string. Use either this or --prd-file."
    ),
    prd_file: Optional[Path] = typer.Option(
        None, 
        "--prd-file", 
        help="Path to the PRD markdown file. Use either this or --prd-content.",
        exists=True, 
        file_okay=True, 
        dir_okay=False, 
        readable=True,
        resolve_path=True
    ),
    output_path: Path = typer.Option(
        Path("dev_client_output"), 
        "--output-path", "-o", 
        help="Directory to save the generated project.",
        resolve_path=True
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v",
        help="Enable verbose output"
    ),
):
    """Generate a system design based on the given requirements."""
    console.print(Panel(
        f"[bold blue]Architect Agent[/bold blue] - Designing project: [cyan]{project_name}[/cyan]",
        border_style="blue"
    ))

    if not prd_content and not prd_file:
        console.print("[red]Error:[/red] Either --prd-content or --prd-file must be provided.", style="bold red")
        raise typer.Exit(code=1)
    if prd_content and prd_file:
        console.print("[red]Error:[/red] Please provide either --prd-content or --prd-file, not both.", style="bold red")
        raise typer.Exit(code=1)

    actual_prd_content = ""
    if prd_file:
        if verbose:
            console.print(f"[dim]Loading PRD from file: {prd_file}[/dim]")
        try:
            actual_prd_content = prd_file.read_text()
        except Exception as e:
            console.print(f"[red]Error reading PRD file {prd_file}:[/red] {e}", style="bold red")
            raise typer.Exit(code=1)
    elif prd_content:
        if verbose:
            console.print("[dim]Using PRD content from argument.[/dim]")
        actual_prd_content = prd_content

    if not actual_prd_content.strip():
        console.print("[red]Error:[/red] PRD content is empty.", style="bold red")
        raise typer.Exit(code=1)

    # Prepare output directory
    final_project_path = output_path / project_name
    try:
        os.makedirs(final_project_path, exist_ok=True)
        if verbose:
            console.print(f"[dim]Project will be generated in: {final_project_path.resolve()}[/dim]")
    except OSError as e:
        console.print(f"[red]Error creating project directory {final_project_path}:[/red] {e}", style="bold red")
        raise typer.Exit(code=1)

    console.print(f"[bold]Initializing Development Agent for '{project_name}'...[/bold]")
    try:
        # For now, DevelopmentAgent doesn't take specific config for PRD path or project name directly in constructor
        # It operates on tasks derived from requirements.
        dev_agent = DevelopmentAgent(name=f"{project_name}DevBot", role="developer_from_prd")
        
        console.print("[bold]Analyzing PRD...[/bold]")
        # The current DevelopmentAgent.analyze_requirements is a placeholder.
        # It doesn't truly parse a PRD into a file structure.
        # We will simulate this by assuming the PRD content itself contains markers
        # for files, similar to the hello_world_prd.md structure.
        # This part will need significant enhancement if the PRD is less structured.

        # --- Placeholder for PRD to File Manifest Logic ---
        # For this iteration, we'll hardcode a simple parser that looks for
        # markdown code blocks with filenames, like in hello_world_prd.md
        # Example: ```python filename=src/main.py
        #            <code>
        #            ```
        # This is a simplification. A real system would need a more robust PRD format or LLM-based interpretation.
        
        import re
        # Regex to find markdown code blocks with a filename attribute
        # It captures the filename, the language (optional), and the code content
        # Pattern: ```(language)? filename=(path/to/filename.ext)
        #          (code_content)
        #          ```
        file_pattern = re.compile(r"```(?:\w+)?\s*filename=([\w\.\-/]+)\s*\n(.*?)\n```", re.DOTALL | re.MULTILINE)
        
        files_to_create = []
        for match in file_pattern.finditer(actual_prd_content):
            relative_path = match.group(1).strip()
            code_content = match.group(2).strip()
            files_to_create.append({"path": relative_path, "content": code_content})

        if not files_to_create:
            console.print("[yellow]Warning:[/yellow] No files found in PRD to generate. Ensure PRD uses 'filename=' in code blocks.")
            # Attempt to use analyze_requirements and generate_code as a fallback for a single file if PRD is simple text
            if len(actual_prd_content.splitlines()) < 20: # Arbitrary small PRD
                 console.print("[dim]Attempting to treat PRD as a single task description...[/dim]")
                 analysis = dev_agent.analyze_requirements(actual_prd_content)
                 # Use the first user story as task, or the whole PRD if no stories
                 task_desc_for_file = analysis.get('user_stories', [actual_prd_content])[0]
                 code_content, _ = dev_agent.generate_code(task_description=task_desc_for_file)
                 # Default filename if not specified
                 default_filename = f"{project_name.lower().replace(' ', '_')}.py"
                 files_to_create.append({"path": default_filename, "content": code_content})
            else:
                 console.print("[red]Error:[/red] PRD did not yield any files to create and is too large for single-file fallback.", style="bold red")
                 raise typer.Exit(code=1)

        console.print(f"[bold]Generating {len(files_to_create)} project files...[/bold]")
        for file_spec in files_to_create:
            file_path_str = file_spec["path"]
            file_content = file_spec["content"]
            
            full_file_path = final_project_path / file_path_str
            
            try:
                # Ensure parent directory exists
                os.makedirs(full_file_path.parent, exist_ok=True)
                full_file_path.write_text(file_content)
                if verbose:
                    console.print(f"  [green]Created:[/green] {full_file_path.relative_to(final_project_path.parent)}")
                else:
                    console.print(f"  [green]Created:[/green] {file_path_str}")
            except OSError as e:
                console.print(f"  [red]Error creating file {full_file_path}:[/red] {e}", style="bold red")
                # Optionally, decide if one error should stop all generation

        console.print(f"\n[bold green]Project '{project_name}' generated successfully at: {final_project_path.resolve()}[/bold green]")
        console.print(Panel(
            f"Project [cyan]{project_name}[/cyan] created at [link=file://{final_project_path.resolve()}]{final_project_path.resolve()}[/link]",
            title="[bold green]Success[/bold green]",
            border_style="green"
        ))

    except Exception as e:
        console.print(f"[red]An unexpected error occurred during project generation:[/red] {str(e)}", style="bold red")
        if verbose:
            import traceback
            console.print(traceback.format_exc())
        raise typer.Exit(code=1)


# This allows the module to be run directly for testing
if __name__ == "__main__":
    app()
