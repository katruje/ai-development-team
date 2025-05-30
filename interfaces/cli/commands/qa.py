"""QA Engineer CLI Commands.

This module provides command-line interface commands for interacting with the
QA Engineer agent. It allows users to run tests, generate test cases, and manage
test coverage from the command line.

The commands are built using Typer and provide rich console output using the
Rich library for better readability and user experience.
"""

import typer
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.table import Table

from agent_core.agents.qa_engineer import QAEngineerAgent
from agent_core.base.message import AgentMessage
from agent_core.base.protocols import AgentRole

app = typer.Typer(name="qa", help="QA Engineer commands")
console = Console()


@app.command("run-tests")
def run_tests(
    test_path: str = typer.Argument(
        "tests/",
        help=(
            "Path to test file or directory to run. Can be a directory containing "
            "test files or a specific test file. Defaults to 'tests/'."
        ),
    ),
    coverage: bool = typer.Option(
        False,
        "--coverage",
        "-c",
        help=(
            "Enable test coverage reporting. Generates a coverage report showing "
            "which parts of the code are covered by tests."
        ),
    ),
    threshold: Optional[float] = typer.Option(
        None,
        "--threshold",
        "-t",
        help=(
            "Set minimum test coverage threshold as a percentage (0-100). "
            "If the actual coverage is below this threshold, the command will fail. "
            "Requires --coverage."
        ),
        min=0,
        max=100,
    ),
):
    """Execute tests and display detailed results.

    This command runs the specified tests and displays a formatted report of the
    results, including pass/fail counts and optional coverage information. The command
    will exit with a non-zero status code if any tests fail or if coverage is below the
    specified threshold.

    Examples:
        # Run all tests in the tests/ directory
        ai-dev-team qa run-tests

        # Run a specific test file
        ai-dev-team qa run-tests tests/test_my_feature.py

        # Run with coverage report
        ai-dev-team qa run-tests --coverage

        # Enforce minimum coverage threshold (fails if coverage < 90%)
        ai-dev-team qa run-tests --coverage --threshold 90
    """
    qa_agent = QAEngineerAgent()

    console.print(f"\n[bold blue]Running tests in {test_path}...[/]\n")

    # Run tests
    message = AgentMessage(
        role=AgentRole.QA_ENGINEER,
        content=f"Running tests in {test_path}",
        metadata={
            "command": "run_tests",
            "data": {"test_path": test_path, "coverage": coverage},
        },
    )

    response = qa_agent.process_message(message)

    if response.metadata.get("command") == "test_results":
        results = response.metadata.get("results", {})

        # Display test results
        table = Table(
            title="Test Results", show_header=True, header_style="bold magenta"
        )
        table.add_column("Metric", style="dim", width=20)
        table.add_column("Value", justify="right")

        table.add_row("Total Tests", str(results["total"]))
        table.add_row("Passed", f"[green]{results['passed']}")
        table.add_row(
            "Failed", f"[red]{results['failed']}" if results["failed"] > 0 else "0"
        )
        table.add_row(
            "Errors", f"[red]{results['errors']}" if results["errors"] > 0 else "0"
        )

        if "coverage" in results and results["coverage"] is not None:
            coverage_percent = results["coverage"]
            coverage_style = "green"
            if threshold and coverage_percent < threshold:
                coverage_style = "red"
            table.add_row("Coverage", f"[{coverage_style}]{coverage_percent}%[/]")

        console.print(table)

        # Check coverage threshold
        if threshold and ("coverage" not in results or results["coverage"] is None):
            console.print(
                (
                    "[yellow]Warning: Coverage threshold specified but no coverage "
                    "data available[/]"
                )
            )
        elif threshold and results["coverage"] < threshold:
            console.print(
                f"[red]Error: Coverage ({results['coverage']}%) "
                f"is below threshold ({threshold}%)[/]"
            )
            raise typer.Exit(code=1)

        if results["failed"] > 0 or results["errors"] > 0:
            raise typer.Exit(code=1)
    else:
        error_message = response.content or response.metadata.get(
            "error", "Unknown error"
        )
        console.print(f"[red]Error: {error_message}[/]")
        raise typer.Exit(code=1)


@app.command("generate-tests")
def generate_tests(
    target_path: str = typer.Argument(
        ...,
        help="Path to the target Python file or module to generate tests for. "
        "This should be the path to the implementation code that needs testing.",
    ),
    test_type: str = typer.Option(
        "unit",
        "--type",
        "-t",
        help=(
            "Type of tests to generate. Supported values: 'unit' (default), 'integration'. "
            "Unit tests test individual components in isolation, while integration tests "
            "verify interactions between components."
        ),
    ),
    output_dir: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help=(
            "Output directory for generated test files. If not specified, tests will be "
            "generated in a 'tests' directory mirroring the source directory structure."
        ),
        file_okay=False,
        dir_okay=True,
        writable=True,
        resolve_path=True,
    ),
):
    """Generate comprehensive test cases for Python code.

    This command analyzes the specified Python module or file and generates appropriate
    test cases based on the implementation. The generated tests include common test
    cases and edge cases to ensure good code coverage.

    The test files are structured according to Python best practices, with test classes
    and methods that follow the naming convention 'test_*' for test discovery.

    Args:
        target_path: Path to the Python file or module to generate tests for.
        test_type: Type of tests to generate. 'unit' for testing individual components
                 in isolation, 'integration' for testing component interactions.
        output_dir: Directory where generated test files will be saved. If not specified,
            tests will be placed in a 'tests' directory mirroring the source structure.

    Examples:
        # Generate unit tests for a module
        ai-dev-team qa generate-tests myproject/utils.py

        # Generate integration tests with custom output directory
        ai-dev-team qa generate-tests myproject/ \
            --type integration --output tests/integration

        # Generate tests for a package
        ai-dev-team qa generate-tests myproject/
    """
    qa_agent = QAEngineerAgent()

    console.print(
        f"\n[bold blue]Generating {test_type} tests for {target_path}...[/]\n"
    )

    # Generate tests
    message = AgentMessage(
        role=AgentRole.QA_ENGINEER,
        content=f"Generating {test_type} tests for {target_path}",
        metadata={
            "command": "generate_tests",
            "data": {"target_path": target_path, "test_type": test_type},
        },
    )

    response = qa_agent.process_message(message)

    if response.metadata.get("command") == "test_generation_result":
        test_path = response.metadata.get("test_path", "unknown")
        console.print(
            f"[green]✓ {response.content or 'Tests generated successfully: ' + str(test_path)}[/]"
        )

        if output_dir:
            console.print("[dim]Note: Output directory option not yet implemented[/]")
    else:
        error_message = response.content or response.metadata.get(
            "error", "Failed to generate tests"
        )
        console.print(f"[red]Error: {error_message}[/]")
        raise typer.Exit(code=1)
