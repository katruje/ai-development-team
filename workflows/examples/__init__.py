"""Hello World workflow implementation."""

import subprocess
from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from jinja2 import Environment, FileSystemLoader


class WorkflowError(Exception):
    """Custom exception for workflow-related errors."""

    pass


class HelloWorldWorkflow:
    """Workflow for generating a Hello World Python package."""

    def __init__(self, config_path: str, output_dir: str = ".") -> None:
        """Initialize the workflow with configuration.

        Args:
            config_path: Path to the workflow configuration file.
            output_dir: Directory where the project will be created.
        """
        self.config_path = Path(config_path)
        self.output_dir = Path(output_dir)
        self.config: Dict[str, Any] = {}
        self.template_env: Optional[Environment] = None

    def load_config(self) -> None:
        """Load and validate the workflow configuration."""
        try:
            with open(self.config_path, "r") as f:
                self.config = yaml.safe_load(f)
        except (yaml.YAMLError, OSError) as e:
            raise WorkflowError(f"Failed to load config: {e}")

    def setup_templates(self) -> None:
        """Set up the Jinja2 template environment."""
        template_dir = self.config_path.parent / "templates"
        if not template_dir.exists():
            raise WorkflowError(f"Template directory not found: {template_dir}")

        self.template_env = Environment(
            loader=FileSystemLoader(template_dir), autoescape=False
        )

    def render_template(
        self, template_name: str, context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Render a template with the given context.

        Args:
            template_name: Name of the template file.
            context: Variables to pass to the template.

        Returns:
            Rendered template as a string.
        """
        if self.template_env is None:
            raise WorkflowError("Template environment not initialized")

        template = self.template_env.get_template(template_name)
        return template.render(**(context or {}))

    def execute_command(self, command: str, cwd: Optional[str] = None) -> None:
        """Execute a shell command.

        Args:
            command: Command to execute.
            cwd: Working directory for the command.

        Raises:
            WorkflowError: If the command fails.
        """
        try:
            subprocess.run(
                command,
                shell=True,
                check=True,
                cwd=cwd,
                capture_output=True,
                text=True,
            )
        except subprocess.CalledProcessError as e:
            raise WorkflowError(f"Command failed with code {e.returncode}: {e.stderr}")

    def run_step(self, step: Dict[str, Any], context: Dict[str, Any]) -> None:
        """Execute a single workflow step.

        Args:
            step: Step configuration.
            context: Template context variables.
        """
        step_name = step.get("name", "unnamed")
        print(f"\n[{step_name}] {step.get('description', '')}")

        if "template" in step and "output" in step:
            # Template rendering step
            output_path = Path(str(step["output"]).format(**context))
            output_path.parent.mkdir(parents=True, exist_ok=True)

            rendered = self.render_template(step["template"], context)
            output_path.write_text(rendered, encoding="utf-8")
            print(f"  ✓ Generated {output_path}")

        elif "commands" in step:
            # Command execution step
            for cmd in step["commands"]:
                cmd = cmd.format(**context)
                print(f"  $ {cmd}")
                self.execute_command(cmd, cwd=self.output_dir)

    def run(self) -> None:
        """Execute the workflow."""
        print("Starting Hello World workflow...")

        try:
            self.load_config()
            self.setup_templates()

            # Create output directory if it doesn't exist
            self.output_dir.mkdir(parents=True, exist_ok=True)

            # Get context from config and add project info
            context = self.config.get("context", {}).copy()
            context.update(
                {
                    "project_name": self.output_dir.name,
                    "package_name": self.output_dir.name.lower().replace("-", "_"),
                }
            )

            # Execute each step in the workflow
            for step in self.config["workflow"]["steps"]:
                self.run_step(step, context)

            print("\n✅ Workflow completed successfully!")
            print(f"Project created at: {self.output_dir.absolute()}")

        except WorkflowError as e:
            print(f"\n❌ Workflow failed: {e}")
            raise


def main() -> None:
    """Run the Hello World workflow."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate a Hello World Python package."
    )
    parser.add_argument(
        "--config",
        default=Path(__file__).parent / "config.yaml",
        help="Path to workflow configuration file",
    )
    parser.add_argument(
        "--output",
        default="hello_world",
        help="Output directory for the generated project",
    )
    args = parser.parse_args()

    workflow = HelloWorldWorkflow(config_path=args.config, output_dir=args.output)
    workflow.run()


if __name__ == "__main__":
    main()
