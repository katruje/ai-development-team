"""Templates for code generation.

This package contains Jinja2 templates used by the DeveloperAgent for code generation.
"""

import os
from pathlib import Path

# Get the directory containing the templates
TEMPLATES_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
