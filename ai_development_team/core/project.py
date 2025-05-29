"""
Project management module.

This module defines the Project class, which represents a software development
project being worked on by the AI Development Team.
"""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging
import yaml

logger = logging.getLogger(__name__)

@dataclass
class Project:
    """
    Represents a software development project.
    
    Attributes:
        name: Name of the project
        description: Brief description of the project
        requirements: Project requirements in natural language
        directory: Base directory for the project files
        metadata: Additional project metadata
        created_at: Timestamp of project creation
        updated_at: Timestamp of last update
    """
    name: str
    description: str = ""
    requirements: str = ""
    directory: Path = Path.cwd()
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        """Initialize project directory and metadata."""
        self.directory = Path(self.directory).absolute()
        self.metadata.setdefault("version", "0.1.0")
        self.metadata.setdefault("status", "initialized")
    
    def initialize(self) -> bool:
        """
        Initialize the project directory structure.
        
        Returns:
            bool: True if initialization was successful
        """
        try:
            self.directory.mkdir(parents=True, exist_ok=True)
            
            # Create basic project structure
            (self.directory / "src").mkdir(exist_ok=True)
            (self.directory / "tests").mkdir(exist_ok=True)
            (self.directory / "docs").mkdir(exist_ok=True)
            
            # Create basic project files
            self._create_readme()
            self._create_config()
            
            self.updated_at = datetime.utcnow()
            logger.info(f"Initialized project '{self.name}' at {self.directory}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize project: {e}")
            return False
    
    def _create_readme(self) -> None:
        """Create a basic README.md file for the project."""
        readme_path = self.directory / "README.md"
        if not readme_path.exists():
            readme_path.write_text(
                f"# {self.name}\n\n"
                f"{self.description}\n\n"
                "## Project Structure\n"
                "- `src/`: Source code\n"
                "- `tests/`: Test files\n"
                "- `docs/`: Documentation\n\n"
                "## Requirements\n"
                f"{self.requirements}"
            )
    
    def _create_config(self) -> None:
        """Create a basic project configuration file."""
        config = {
            "name": self.name,
            "description": self.description,
            "version": self.metadata["version"],
            "status": self.metadata["status"],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "requirements": self.requirements
        }
        
        config_path = self.directory / "project_config.yaml"
        with open(config_path, 'w') as f:
            yaml.safe_dump(config, f, sort_keys=False)
    
    def update_status(self, status: str) -> None:
        """
        Update the project status.
        
        Args:
            status: New status (e.g., 'in_progress', 'completed', 'on_hold')
        """
        self.metadata["status"] = status
        self.updated_at = datetime.utcnow()
        logger.info(f"Updated project status to '{status}' for '{self.name}'")
