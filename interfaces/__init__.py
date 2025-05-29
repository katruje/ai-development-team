"""Interfaces package for the AI Development Team."""

# This file makes the interfaces directory a Python package
# and can be used to expose the main CLI app

# Import the main CLI app to make it available when the package is imported
from .cli.main import app as cli_app  # noqa: F401

__all__ = ["cli_app"]
