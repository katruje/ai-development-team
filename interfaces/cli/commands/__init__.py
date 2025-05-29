"""CLI command modules for the AI Development Team."""

import typer

# Import command modules here to register them with Typer
from . import architect as architect_commands

# Expose the app for registration in main.py
app = typer.Typer()
app.add_typer(architect_commands.app, name="architect", help="Architect agent commands")
