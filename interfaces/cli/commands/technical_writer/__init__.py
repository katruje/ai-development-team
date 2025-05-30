"""Technical Writer CLI Commands.

This module provides command-line interface commands for interacting with the
Technical Writer agent. It allows users to generate, validate, and manage
technical documentation from the command line.

The commands are built using Typer and provide rich console output using the
Rich library for better readability and user experience.
"""

import typer
from pathlib import Path
from typing import Optional

from rich.console import Console

from agent_core.agents.technical_writer import TechnicalWriterAgent
from agent_core.base.message import AgentMessage
from agent_core.base.protocols import AgentRole

app = typer.Typer(name="docs", help="Technical Writer commands")
console = Console()


@app.command("generate")
def generate_docs(
    target_path: str = typer.Argument(
        ...,
        help=(
            "Path to the Python file or package to generate documentation for. "
            "This should be the path to the implementation code that needs "
            "documentation."
        ),
    ),
    output_format: str = typer.Option(
        "markdown",
        "--format",
        "-f",
        help=(
            "Output format for the documentation. "
            "Supported values: 'markdown' (default), 'html', 'pdf'."
        ),
    ),
    output_dir: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help=(
            "Output directory for generated documentation. "
            "If not specified, documentation will be generated in 'docs/'."
        ),
        file_okay=False,
        dir_okay=True,
        writable=True,
        resolve_path=True,
    ),
):
    """Generate comprehensive documentation for Python code.

    This command analyzes the specified Python module or package and generates
    documentation in the specified format. The generated documentation includes
    API references, usage examples, and module/package documentation.

    Examples:
        # Generate markdown documentation for a package
        ai-dev-team docs generate mypackage/

        # Generate HTML documentation with custom output directory
        ai-dev-team docs generate mymodule.py --format html --output docs/html

        # Generate PDF documentation
        ai-dev-team docs generate myproject/ --format pdf
    """
    agent = TechnicalWriterAgent()

    console.print(
        "\n"
        f"[bold blue]Generating {output_format} documentation for "
        f"{target_path}...[/]\n"
    )

    message = AgentMessage(
        role=AgentRole.TECHNICAL_WRITER,
        content=f"Generating {output_format} documentation for {target_path}",
        metadata={
            "command": "generate_docs",
            "data": {
                "target_path": target_path,
                "output_format": output_format,
                "output_dir": str(output_dir) if output_dir else None,
            },
        },
    )

    response = agent.process_message(message)

    if response.metadata.get("command") == "documentation_generated":
        output_path = response.metadata.get("output_dir", "docs/generated")
        console.print(f"[green]✓ {response.content}. Output at: {output_path}[/]")
    else:
        console.print(f"[red]Error: {response.content}[/]")
        raise typer.Exit(code=1)


@app.command("validate")
def validate_docs(
    target_path: str = typer.Argument(
        ".",
        help="Path to the directory or file to validate documentation for. "
        "Defaults to current directory.",
    )
):
    """Validate existing documentation for completeness and accuracy.

    This command checks the documentation in the specified directory or file
    for common issues such as missing docstrings, incomplete documentation,
    and outdated examples.

    Examples:
        # Validate documentation in the current directory
        ai-dev-team docs validate

        # Validate documentation for a specific module
        ai-dev-team docs validate mymodule.py
    """
    agent = TechnicalWriterAgent()

    console.print(f"\n[bold blue]Validating documentation in {target_path}...[/]\n")

    message = AgentMessage(
        role=AgentRole.TECHNICAL_WRITER,
        content=f"Validating documentation in {target_path}",
        metadata={"command": "validate_docs", "data": {"target_path": target_path}},
    )

    response = agent.process_message(message)

    if response.metadata.get("command") == "validation_result":
        warnings = response.metadata.get("warnings", [])
        errors = response.metadata.get("errors", [])

        if not warnings and not errors:
            console.print("[green]✓ Documentation validation passed with no issues[/]")
        else:
            if warnings:
                console.print("[yellow]Warnings:[/]")
                for warning in warnings:
                    console.print(f"  • {warning}")

            if errors:
                console.print("\n[red]Errors:[/]")
                for error in errors:
                    console.print(f"  • {error}")

                console.print("\n[red]✗ Documentation validation failed[/]")
                raise typer.Exit(code=1)
            else:
                console.print(
                    "\n[yellow]Documentation validation completed with warnings[/]"
                )
    else:
        console.print(f"[red]Error: {response.content}[/]")
        raise typer.Exit(code=1)


@app.command("update-readme")
def update_readme(
    project_root: str = typer.Argument(
        ".", help="Root directory of the project. Defaults to current directory."
    )
):
    """Update the project's README file with current project information.

    This command generates or updates the README.md file in the specified
    directory with information about the project, including:
    - Project name and description
    - Installation instructions
    - Usage examples
    - Development setup
    - Contributing guidelines
    - License information

    Examples:
        # Update README in the current directory
        ai-dev-team docs update-readme

        # Update README for a specific project
        ai-dev-team docs update-readme /path/to/project
    """
    agent = TechnicalWriterAgent()

    console.print(f"\n[bold blue]Updating README in {project_root}...[/]\n")

    message = AgentMessage(
        role=AgentRole.TECHNICAL_WRITER,
        content=f"Updating README in {project_root}",
        metadata={"command": "update_readme", "data": {"project_root": project_root}},
    )

    response = agent.process_message(message)

    if response.metadata.get("command") == "readme_updated":
        console.print(f"[green]✓ {response.content}[/]")
    else:
        console.print(f"[red]Error: {response.content}[/]")
        raise typer.Exit(code=1)
