"""Architect Agent implementation."""

import logging
import ast
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from rich.console import Console
from rich.table import Table

from agent_core.base import Agent, AgentContext, AgentMessage, AgentRole

logger = logging.getLogger(__name__)
console = Console()


class ProjectAnalyzer:
    """Helper class for analyzing project structure and dependencies."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.python_files: List[Path] = []
        self.imports: Set[str] = set()
        self.dependencies: Dict[str, str] = {}

    def analyze(self) -> None:
        """Analyze the project structure and dependencies."""
        self._find_python_files()
        self._analyze_imports()
        self._analyze_dependencies()

    def _find_python_files(self) -> None:
        """Find all Python files in the project."""
        self.python_files = list(self.project_root.rglob("*.py"))

    def _analyze_imports(self) -> None:
        """Analyze imports in Python files."""
        for py_file in self.python_files:
            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    node = ast.parse(f.read(), filename=str(py_file))

                for n in ast.walk(node):
                    if isinstance(n, (ast.Import, ast.ImportFrom)):
                        if isinstance(n, ast.Import):
                            for name in n.names:
                                self.imports.add(name.name.split(".")[0])
                        else:
                            module = n.module.split(".")[0] if n.module else ""
                            if module:
                                self.imports.add(module)
            except (SyntaxError, UnicodeDecodeError):
                continue

    def _analyze_dependencies(self) -> None:
        """Analyze project dependencies from requirements and imports."""
        # Check for requirements files
        req_files = [
            self.project_root / "requirements.txt",
            self.project_root / "pyproject.toml",
            self.project_root / "setup.py",
        ]

        for req_file in req_files:
            if req_file.exists():
                if req_file.name == "requirements.txt":
                    self._parse_requirements_txt(req_file)
                elif req_file.name == "pyproject.toml":
                    self._parse_pyproject_toml(req_file)
                elif req_file.name == "setup.py":
                    self._parse_setup_py(req_file)

    def _parse_requirements_txt(self, file_path: Path) -> None:
        """Parse requirements.txt file."""
        try:
            with open(file_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        pkg = re.split(r"[<>=!~]", line)[0].strip()
                        if pkg:
                            self.dependencies[pkg] = "requirements.txt"
        except Exception:
            pass

    def _parse_pyproject_toml(self, file_path: Path) -> None:
        """Parse pyproject.toml file."""
        try:
            import tomli

            with open(file_path, "rb") as f:
                data = tomli.load(f)
                if "project" in data and "dependencies" in data["project"]:
                    for dep in data["project"]["dependencies"]:
                        pkg = (
                            dep.split(">=")[0]
                            .split(">")[0]
                            .split("<=")[0]
                            .split("<")[0]
                            .split("~=")[0]
                            .split("!=")[0]
                        )
                        self.dependencies[pkg] = "pyproject.toml"
        except Exception:
            pass

    def _parse_setup_py(self, file_path: Path) -> None:
        """Parse setup.py file (simplified)."""
        try:
            with open(file_path, "r") as f:
                content = f.read()
                # Simple regex to find install_requires
                matches = re.findall(
                    r"install_requires\s*=\s*\[(.*?)\]", content, re.DOTALL
                )
                if matches:
                    for match in matches[0].split(","):
                        pkg = match.strip().strip("'\"")
                        if pkg and not pkg.startswith("#"):
                            pkg = re.split(r"[<>=!~]", pkg)[0].strip()
                            self.dependencies[pkg] = "setup.py"
        except Exception:
            pass

    def get_analysis(self) -> Dict[str, Any]:
        """Get the analysis results."""
        return {
            "python_files": len(self.python_files),
            "imports": sorted(self.imports),
            "dependencies": self.dependencies,
            "project_structure": self._get_project_structure(),
        }

    def _get_project_structure(self) -> List[Dict[str, Any]]:
        """Get the project structure as a list of dicts."""
        structure = []
        for path in sorted(self.project_root.iterdir()):
            if path.name.startswith(
                (".", "__pycache__", "venv", ".venv", "env", ".env")
            ):
                continue
            structure.append(self._get_path_info(path))
        return structure

    def _get_path_info(self, path: Path, depth: int = 0) -> Dict[str, Any]:
        """Get info about a path."""
        info = {
            "name": path.name,
            "type": "directory" if path.is_dir() else "file",
            "size": path.stat().st_size if path.is_file() else 0,
            "children": [],
        }

        if path.is_dir() and depth < 3:  # Limit recursion depth
            try:
                for child in sorted(path.iterdir()):
                    if child.name.startswith("."):
                        continue
                    info["children"].append(self._get_path_info(child, depth + 1))
            except (PermissionError, OSError):
                pass

        return info


class ArchitectAgent(Agent):
    """Agent responsible for system architecture and design decisions."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the Architect agent."""
        super().__init__(config or {})
        self._project_structure = {}

    @property
    def role(self) -> AgentRole:
        """Return the role of this agent."""
        return AgentRole.ARCHITECT

    async def _process_message(
        self, message: AgentMessage, context: AgentContext
    ) -> AgentMessage:
        """Process an incoming message and return a response."""
        content = message.content.lower()

        if any(
            term in content
            for term in ["project structure", "show project", "list files"]
        ):
            return await self._handle_project_structure(context)
        if "analyze" in content or "dependencies" in content:
            return await self._analyze_project(context)
        if any(term in content for term in ["help", "what can you do", "capabilities"]):
            return self._get_help_message()

        return AgentMessage(
            role=self.role,
            content=(
                "I'm the Architect agent. I can help analyze your project structure, "
                "dependencies, and provide architectural guidance. Try asking me to "
                "'analyze the project' or 'show project structure'."
            ),
        )

    async def _analyze_project(self, context: AgentContext) -> AgentMessage:
        """Analyze the project structure and dependencies."""
        project_root = Path(context.project_root)

        if not project_root.exists():
            return AgentMessage(
                role=self.role, content=f"Project directory not found: {project_root}"
            )

        analyzer = ProjectAnalyzer(project_root)
        analyzer.analyze()
        analysis = analyzer.get_analysis()

        # Create a formatted report
        console = Console()
        with console.capture() as capture:
            # Project overview
            console.print("\n[bold blue]Project Analysis[/]\n")

            # Basic info
            table = Table(show_header=False, box=None)
            table.add_column(style="cyan", width=20)
            table.add_column()

            table.add_row("Python Files", str(analysis["python_files"]))
            table.add_row("Dependencies", str(len(analysis["dependencies"])))
            table.add_row(
                "Imports",
                ", ".join(analysis["imports"][:5])
                + ("..." if len(analysis["imports"]) > 5 else ""),
            )

            console.print(table)

            # Dependencies
            if analysis["dependencies"]:
                console.print("\n[bold]Dependencies:[/]")
                deps_table = Table(show_header=True, header_style="bold magenta")
                deps_table.add_column("Package", style="cyan")
                deps_table.add_column("Source")

                for pkg, source in analysis["dependencies"].items():
                    deps_table.add_row(pkg, source)
                console.print(deps_table)

            # Project structure summary
            console.print("\n[bold]Project Structure:[/]")
            self._print_project_tree(analysis["project_structure"])

        return AgentMessage(
            role=self.role, content=f"Project Analysis:\n{capture.get()}"
        )

    def _print_project_tree(self, structure: List[Dict], prefix: str = "") -> None:
        """Print project structure as a tree."""
        console = Console()
        for i, item in enumerate(structure):
            is_last = i == len(structure) - 1
            marker = "└── " if is_last else "├── "

            if item["type"] == "directory":
                console.print(f"{prefix}{marker}[bold green]{item['name']}/[/]")
                new_prefix = prefix + ("    " if is_last else "│   ")
                self._print_project_tree(item["children"], new_prefix)
            else:
                console.print(f"{prefix}{marker}[yellow]{item['name']}[/]")

    async def _handle_project_structure(self, context: AgentContext) -> AgentMessage:
        """Handle requests to show the project structure."""
        project_root = Path(context.project_root)

        if not project_root.exists():
            return AgentMessage(
                role=self.role, content=f"Project directory not found: {project_root}"
            )

        analyzer = ProjectAnalyzer(project_root)
        analyzer.analyze()
        analysis = analyzer.get_analysis()

        # Create a tree structure
        console = Console()
        with console.capture() as capture:
            console.print("\n[bold blue]Project Structure:[/]\n")
            self._print_project_tree(analysis["project_structure"])

        return AgentMessage(role=self.role, content=f"{capture.get()}")

    def _get_help_message(self) -> AgentMessage:
        """Return help message with available commands."""
        help_text = """[bold]Architect Agent Help[/bold]

Available commands:
- [cyan]Show project structure[/] - Display the project file structure
- [cyan]Analyze project[/] - Analyze project dependencies and structure
- [cyan]Help[/] - Show this help message

You can ask me to analyze your project's architecture, suggest improvements,
or help with project setup and organization."""

        return AgentMessage(role=self.role, content=help_text)
