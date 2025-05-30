"""Developer Agent implementation."""

import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Union

import jinja2

from agent_core.base import Agent, AgentContext, AgentMessage, AgentRole
from agent_core.agents.developer.templates import TEMPLATES_DIR

# Configure Jinja2 environment
env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(TEMPLATES_DIR),
    trim_blocks=True,
    lstrip_blocks=True,
    keep_trailing_newline=True,
)

logger = logging.getLogger(__name__)


class DeveloperAgent(Agent):
    """Agent responsible for software development tasks.  # noqa: E501

    The DeveloperAgent handles various aspects of the software development lifecycle,
    including requirements analysis, code generation, code review, and knowledge management.
    It maintains its own memory and knowledge base
    to provide context-aware assistance.

    Attributes:
        name (str): The name of the agent.
        skills (List[str]): List of programming languages and technologies
            the agent is skilled in.
        memory (Dict[str, Any]): Internal memory for tracking conversation and tasks.
        knowledge_base (Dict[str, Any]): Storage for domain knowledge and code snippets.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None, **kwargs):
        """Initialize the DeveloperAgent with configuration.

        The agent can be configured via a config dictionary or keyword arguments.

        If both are provided, keyword arguments take precedence.

        Args:
            config: Configuration dictionary. May contain:
                - name: (str) Name of the agent
                - skills: (List[str]) List of programming languages/technologies
                - verbose: (bool) Enable verbose output
                - templates_dir: (str) Path to custom templates directory
            **kwargs: Additional configuration as keyword arguments
                (will be merged into config)

        Example:
            ```python
            # Initialize with config dictionary
            agent = DeveloperAgent({
                "name": "PythonDev",
                "skills": ["python", "fastapi", "sqlalchemy"],
                "templates_dir": "path/to/custom/templates"
            })

            # Or with keyword arguments
            agent = DeveloperAgent(name="PythonDev", skills=["python"])
            ```
        """
        # Handle both config dict and direct keyword arguments
        if config is None:
            config = {}
        config.update(kwargs)  # Allow direct kwargs to override config dict

        super().__init__(config)
        self.name = config.get("name", "DeveloperAgent")
        self.skills = config.get("skills", ["python"])
        self.memory = {
            "conversation": [],
            "tasks": {},
            "initial_requirements": "",
            "analyzed_requirements": {},
            "environment_checked": False,
        }
        self.knowledge_base = {}

        # Configure template environment
        templates_dir = config.get("templates_dir")
        if templates_dir and os.path.isdir(templates_dir):
            self.env = jinja2.Environment(
                loader=jinja2.FileSystemLoader(templates_dir),
                trim_blocks=True,
                lstrip_blocks=True,
                keep_trailing_newline=True,
            )
        else:
            self.env = env

    @property
    def role(self) -> AgentRole:
        """Return the role of this agent."""
        return AgentRole.DEVELOPER

    async def _process_message(
        self, message: AgentMessage, context: AgentContext
    ) -> AgentMessage:
        """Process an incoming message and generate an appropriate response.

        This method handles different types of development-related requests and routes them
        to the appropriate handler methods. It's the main entry point for the agent's functionality.

        Args:
            message: The incoming message containing the request and metadata
            context: The current execution context, including conversation history

        Returns:
            AgentMessage: The response message containing the result of the operation

        Raises:
            ValueError: If the message content is invalid or missing required fields

        Example:
            ```python
            response = await agent._process_message(message, context)
            print(response.content)
            ```
        """
        response = AgentMessage(role=self.role, content="")

        if not message.content:
            response.content = "Error: Empty message received."
            return response

        # Split command and arguments
        parts = message.content.strip().split()
        command = parts[0].lower() if parts else ""
        args = parts[1:] if len(parts) > 1 else []
        full_command = " ".join(parts)

        try:
            if command == "help":
                response.content = self._get_help_message()

            elif command == "check-env":
                env_status = self.check_environment()
                response.content = "Environment check results:\n"
                response.content += f"Python version: {env_status['python_version']}\n"
                response.content += f"Virtual environment: {'Yes' if env_status['virtual_env'] else 'No'}\n"
                if env_status["venv_path"]:
                    response.content += (
                        f"Virtual environment path: {env_status['venv_path']}\n"
                    )

                response.content += "\nDependencies:\n"
                for pkg, version in env_status["dependencies"].items():
                    response.content += f"- {pkg}: {version}\n"

                if env_status["issues"]:
                    response.content += "\nIssues found:\n"
                    for issue in env_status["issues"]:
                        response.content += f"- {issue}\n"
                else:
                    response.content += "\nNo issues found. Environment looks good!\n"

            elif command == "generate-from-template":
                if len(args) < 2:
                    response.content = "Error: 'generate-from-template' requires template name and output path"
                    return response

                template_name = args[0]
                output_path = args[1]

                # Simple context for the template
                context = {
                    "module_name": Path(output_path).stem,
                    "class_name": Path(output_path).stem.title().replace("_", ""),
                    "description": f"Generated {Path(output_path).stem} module",
                    "class_description": f"Implementation of {Path(output_path).stem}.",
                    "init_params": [
                        ("param1", "str", "First parameter"),
                        ("param2", "int", "Second parameter"),
                    ],
                    "methods": [
                        {
                            "name": "example_method",
                            "params": [
                                ("self", "Any", ""),
                                ("param", "str", "Example parameter"),
                            ],
                            "return_type": "bool",
                            "return_description": "True if successful, False otherwise",
                            "description": "Example method that does something.",
                            "raises": [
                                {
                                    "type": "ValueError",
                                    "description": "If param is empty",
                                }
                            ],
                            "body": '        if not param:\n            raise ValueError("param cannot be empty")\n        return True',
                        }
                    ],
                    "functions": [
                        {
                            "name": "example_function",
                            "params": [
                                ("param1", "str", "First parameter"),
                                ("param2", "int", "Second parameter"),
                            ],
                            "return_type": "bool",
                            "return_description": "True if successful",
                            "description": "Example function that does something.",
                            "raises": [
                                {
                                    "type": "ValueError",
                                    "description": "If param1 is empty",
                                }
                            ],
                            "example": {
                                "name": "example_function",
                                "args": ['"test"', "42"],
                                "output": "True",
                            },
                            "body": '    if not param1:\n        raise ValueError("param1 cannot be empty")\n    return True',
                        }
                    ],
                    "imports": [
                        "import os",
                        "from pathlib import Path",
                        "from typing import Any, Dict, List, Optional, Union",
                    ],
                }

                try:
                    result = self.generate_from_template(
                        template_name=template_name,
                        output_path=output_path,
                        context=context,
                        overwrite="--overwrite" in args,
                    )

                    if result["success"]:
                        response.content = f"Successfully generated {result['output_path']} from template {template_name}"
                    else:
                        response.content = (
                            f"Error generating from template: {result['error']}"
                        )

                except Exception as e:
                    response.content = f"Error generating from template: {str(e)}"
                    logger.error(response.content, exc_info=True)

            elif command.startswith("analyze"):
                requirements = full_command.replace("analyze", "").strip()
                if not requirements:
                    response.content = "Error: No requirements provided for analysis"
                    return response

                analysis = self.analyze_requirements(requirements)
                response.content = "Analyzed requirements:\n"
                for key, value in analysis.items():
                    response.content += f"\n{key.title().replace('_', ' ')}:\n"
                    if isinstance(value, list):
                        for item in value:
                            response.content += f"- {item}\n"
                    else:
                        response.content += f"{value}\n"

            elif full_command.startswith("create file"):
                # Handle the create file command
                parts = full_command.split(" with content: ", 1)
                
                if len(parts) == 1:
                    # Handle case with no content (just filename)
                    file_path_part = parts[0].replace("create file", "").strip()
                    file_content = ""
                else:
                    # Handle case with content
                    file_path_part = parts[0].replace("create file", "").strip()
                    file_content = parts[1].strip()

                if not file_path_part:
                    response.content = "Error: File path not specified for 'create file' command."
                    return response

                # Determine the full path relative to the project root in context
                project_root = getattr(context, 'project_root', None)
                if project_root:
                    full_file_path = Path(project_root) / file_path_part
                else:
                    full_file_path = Path(file_path_part)

                try:
                    # Create parent directories if they don't exist
                    full_file_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    self.write_code(
                        str(full_file_path),
                        file_content,
                        overwrite="--overwrite" in args,
                    )
                    response.content = f"File created successfully: {file_path_part}"
                except FileExistsError:
                    response.content = (
                        f"Error: File already exists: {file_path_part}. "
                        "Use --overwrite flag to overwrite."
                    )
                except Exception as e:
                    logger.error(
                        f"Error creating file {file_path_part}: {e}", exc_info=True
                    )
                    response.content = f"Error creating file {file_path_part}: {e}"

            elif command.startswith("generate"):
                task = full_command.replace("generate", "").strip()
                if not task:
                    response.content = "Error: No task provided for code generation"
                    return response

                # Pass None for context as AgentContext is a dataclass and generate_code doesn't use it yet
                code, metadata = self.generate_code(task, None)
                response.content = f"Generated code for task: {task}\n\n{code}"
                response.metadata = metadata

            elif command.startswith("write"):
                parts = full_command.split(maxsplit=2)
                if len(parts) < 3:
                    response.content = (
                        "Error: 'write' command needs file path and content"
                    )
                else:
                    file_path = parts[1]
                    code_content = parts[2]
                    if self.write_code(
                        file_path, code_content, overwrite="--overwrite" in args
                    ):
                        response.content = f"Successfully wrote code to {file_path}"
                    else:
                        response.content = f"Failed to write code to {file_path}"

            else:
                response.content = (
                    "Unknown command. Type 'help' for available commands."
                )
        except Exception as e:
            logger.error(f"Error processing message: {e}", exc_info=True)
            response.content = f"An error occurred: {e}"

        return response

    def analyze_requirements(self, requirements: str) -> Dict[str, Any]:
        """Analyze natural language requirements and extract structured information.

        This method processes free-form requirements text and identifies key components
        such as features, constraints, and acceptance criteria. It's useful for
        transforming initial client requests into a more actionable format.

        Args:
            requirements: A string containing the natural language requirements.

        Returns:
            A dictionary containing the structured analysis, including:
                - user_stories: List of identified user stories
                - acceptance_criteria: List of acceptance criteria for each story
                - technical_requirements: List of technical constraints or needs
                - open_questions: List of questions for clarification

        Example:
            ```python
            requirements = ("The system should allow users to register and login.\n"
                         "- Users must provide a unique email and password.\n"
                         "- Password must be at least 8 characters long.\n"
                         "- Needs documentation")
            analysis = agent.analyze_requirements(requirements)
            print(analysis['features'])
            ```
        """
        self.memory["initial_requirements"] = requirements

        # Simple analysis - in a real implementation, this would use an LLM or NLP library
        analysis = {
            "user_stories": ["As a user, I can register with email and password."],
            "acceptance_criteria": ["Unique email required", "Password >= 8 chars"],
            "technical_requirements": ["Database for user storage"],
            "open_questions": ["What are the password complexity rules beyond length?"],
        }
        self.memory["analyzed_requirements"] = analysis
        return analysis

    def generate_code(
        self, task: str, context: Optional[Dict] = None
    ) -> Tuple[str, Dict]:
        """Generate code based on the given task description.

        This method takes a natural language description of a coding task and generates
        appropriate code. The generated code includes relevant documentation and follows
        best practices for the specified language.

        Args:
            task: A string describing the code to generate
            context: Optional dictionary containing additional context, such as:
                - language: (str) Target programming language (e.g., "python")
                - project_structure: (dict) Overview of existing project files/folders
                - dependencies: (list) List of project dependencies

        Returns:
            A tuple containing:
                - code: (str) The generated code string
                - metadata: (dict) Information about the generated code (e.g., language, dependencies)

        Example:
            ```python
            code, metadata = agent.generate_code(
                "Create a function that calculates factorial",
                {"language": "python"}
            )
            print(code)
            ```
        """
        task_id = str(len(self.memory["tasks"]) + 1)
        self.memory["tasks"][task_id] = {"description": task, "status": "in_progress"}

        # Simple code generation - in a real implementation, this would use an LLM
        if "test" in task.lower():
            function_name = "test_" + "".join(
                word.lower() for word in task.split()[:3] if word.lower() != "test"
            )
        else:
            function_name = "_" + "".join(word.lower() for word in task.split()[:3])

        code = f"def {function_name}():"
        code += f'\n    """{task}"""'
        code += "\n    pass  # TODO: Implement this function\n"

        metadata = {
            "language": "python",
            "function_name": function_name,
            "task_id": task_id,
        }

        self.memory["tasks"][task_id]["status"] = "completed"
        return code, metadata

    def write_code(self, file_path: str, code: str, overwrite: bool = False) -> None:
        """Write generated code to a file with proper error handling.

        This method handles file operations including creating directories if they don't exist
        and checking for file existence before writing. It maintains a log of all file operations
        in the agent's memory.

        Args:
            file_path: Path where the file should be written. Can be relative or absolute.
            code: The code content to write to the file
            overwrite: If False (default), raises an error if file exists.
                     If True, overwrites existing files.

        Raises:
            FileExistsError: If the file already exists and overwrite is False
            PermissionError: If the agent doesn't have permission to write to the location

        Example:
            ```python
            # Write to a new file
            agent.write_code("utils/math_helpers.py", "def add(a, b): return a + b")

            # Overwrite existing file
            agent.write_code("existing.py", "new code", overwrite=True)
            ```
        """
        file_path_obj = Path(file_path)
        if file_path_obj.exists() and not overwrite:
            raise FileExistsError(
                f"File {file_path_obj} already exists and overwrite=False"
            )

        try:
            file_path_obj.parent.mkdir(parents=True, exist_ok=True)
            file_path_obj.write_text(code, encoding="utf-8")
            logger.info(
                f"Successfully wrote code to {file_path_obj}"
            )  # Add success log
            return True
        except IOError as e:  # Catch IOError specifically to re-raise
            logger.error(f"IOError writing to {file_path_obj}: {str(e)}", exc_info=True)
            raise  # Re-raise the IOError
        except Exception as e:  # Catch other potential exceptions
            logger.error(
                f"Unexpected error writing to {file_path_obj}: {str(e)}", exc_info=True
            )
            raise  # Re-raise other exceptions

    def review_code(self, code: str) -> Dict[str, Any]:
        """Review the given code.

        Args:
            code: The code to review.

        Returns:
            Dict containing review results.
        """
        # Simple review - in a real implementation, this would be more sophisticated
        return {
            "status": "reviewed",
            "feedback": "Code looks good overall.",
            "suggestions": [
                "Consider adding more comments.",
                "Add error handling where necessary.",
            ],
        }

    def update_knowledge(self, knowledge: Dict[str, Any]) -> None:
        """Update the agent's knowledge base.

        Args:
            knowledge: Dictionary of knowledge to add/update.
        """
        self.knowledge_base.update(knowledge)

    def check_environment(self) -> Dict[str, Any]:
        """Check if the development environment is properly set up.

        Returns:
            Dict containing environment check results with the following keys:
                - python_version: str - Current Python version
                - virtual_env: bool - Whether running in a virtual environment
                - venv_path: Optional[str] - Path to virtual environment if active
                - dependencies: Dict[str, str] - Installed package versions
                - issues: List[str] - List of any environment issues found
        """
        import importlib.metadata

        result = {
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "virtual_env": hasattr(sys, "real_prefix")
            or (hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix),
            "venv_path": os.environ.get("VIRTUAL_ENV"),
            "dependencies": {},
            "issues": [],
        }

        # Check required packages
        required_packages = ["jinja2", "typer", "rich"]
        for pkg in required_packages:
            try:
                version = importlib.metadata.version(pkg)
                result["dependencies"][pkg] = version
            except importlib.metadata.PackageNotFoundError:
                result["issues"].append(f"Missing required package: {pkg}")

        # Check virtual environment
        if not result["virtual_env"] and not result["venv_path"]:
            result["issues"].append(
                "Not running in a virtual environment. "
                "It's recommended to use a virtual environment for development."
            )

        # Check Python version
        if sys.version_info < (3, 9):
            result["issues"].append(
                f"Python 3.9+ is required. Current version: {result['python_version']}"
            )

        self.memory["environment_checked"] = True
        self.memory["environment_status"] = result

        return result

    def generate_from_template(
        self,
        template_name: str,
        output_path: Union[str, Path],
        context: Optional[Dict[str, Any]] = None,
        overwrite: bool = False,
    ) -> Dict[str, Any]:
        """Generate code from a template file.

        Args:
            template_name: Name of the template file (e.g., 'python_module.py.j2')
            output_path: Path where the generated file should be saved
            context: Dictionary of variables to pass to the template
            overwrite: Whether to overwrite existing files

        Returns:
            Dict containing:
                - success: bool - Whether generation was successful
                - output_path: str - Path to the generated file
                - error: Optional[str] - Error message if generation failed

        Raises:
            FileExistsError: If output file exists and overwrite is False
            jinja2.TemplateNotFound: If the template doesn't exist
        """
        output_path = Path(output_path)

        # Check if output file exists
        if output_path.exists() and not overwrite:
            raise FileExistsError(
                f"File {output_path} already exists and overwrite=False"
            )

        try:
            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Prepare context with default values
            default_context = {
                "timestamp": datetime.now().isoformat(),
                "agent_name": self.name,
            }
            if context:
                default_context.update(context)

            # Render template
            template = self.env.get_template(template_name)
            rendered = template.render(**default_context)

            # Write to file
            output_path.write_text(rendered, encoding="utf-8")

            return {"success": True, "output_path": str(output_path), "error": None}

        except Exception as e:
            logger.error(
                f"Error generating from template {template_name}: {e}", exc_info=True
            )
            return {"success": False, "output_path": str(output_path), "error": str(e)}

    def _get_help_message(self) -> str:
        """Return help message with available commands."""
        help_msg = """Available commands:
- help: Show this help message
- analyze <requirements>: Analyze software requirements
- generate <task>: Generate code for the given task
- check-env: Check development environment
- generate-from-template <template> <output>: Generate code from a template
"""
        return help_msg
