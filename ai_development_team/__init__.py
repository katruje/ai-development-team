"""
AI Development Team - A virtual software development organization.

This package provides tools for AI-assisted software development, enabling
non-technical users to describe their software needs and have AI agents
develop the required software through iterative feedback cycles.
"""

__version__ = "0.1.0"

# Core functionality imports
from .core.agent import DevelopmentAgent
from .core.project import Project
from .core.workflow import DevelopmentWorkflow

__all__ = [
    "DevelopmentAgent",
    "Project",
    "DevelopmentWorkflow",
    "__version__"
]
