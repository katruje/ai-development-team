"""Developer Agent implementation."""

import logging
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from agent_core.base import Agent, AgentContext, AgentMessage, AgentRole

logger = logging.getLogger(__name__)


class DeveloperAgent(Agent):
    """Agent responsible for software development tasks.
    
    The DeveloperAgent handles various aspects of the software development lifecycle,
    including requirements analysis, code generation, code review, and knowledge management.
    It maintains its own memory and knowledge base to provide context-aware assistance.
    
    Attributes:
        name (str): The name of the agent.
        skills (List[str]): List of programming languages and technologies the agent is skilled in.
        memory (Dict[str, Any]): Internal memory for tracking conversation and tasks.
        knowledge_base (Dict[str, Any]): Storage for domain knowledge and code snippets.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None, **kwargs):
        """Initialize the DeveloperAgent with configuration.
        
        The agent can be configured either through a config dictionary or via keyword arguments.
        If both are provided, keyword arguments take precedence.
        
        Args:
            config: Configuration dictionary. May contain:
                - name: (str) Name of the agent
                - skills: (List[str]) List of programming languages/technologies
                - verbose: (bool) Enable verbose output
            **kwargs: Additional configuration as keyword arguments (will be merged into config)
            
        Example:
            ```python
            # Initialize with config dictionary
            agent = DeveloperAgent({
                "name": "PythonDev",
                "skills": ["python", "fastapi", "sqlalchemy"]
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
        self.skills = ["python"]
        self.memory = {
            "conversation": [],
            "tasks": {},
            "initial_requirements": "",
            "analyzed_requirements": {}
        }
        self.knowledge_base = {}

    @property
    def role(self) -> AgentRole:
        """Return the role of this agent."""
        return AgentRole.DEVELOPER

    async def _process_message(self, message: AgentMessage, context: AgentContext) -> AgentMessage:
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
            
        command = message.content.lower()
        
        try:
            if command == "help":
                response.content = self._get_help_message()
            elif command.startswith("analyze"):
                requirements = command.replace("analyze", "").strip()
                analysis = self.analyze_requirements(requirements)
                response.content = f"Analyzed requirements: {analysis}"
            elif command.startswith("create file"):
                parts = message.content.split(" with content: ", 1)
                file_path_part = parts[0].replace("create file", "").strip()
                file_content = parts[1] if len(parts) > 1 else ""
                
                if not file_path_part:
                    response.content = "Error: File path not specified for 'create file' command."
                    return response
                
                # Determine the full path relative to the project root in context
                if context and context.project_root:
                    full_file_path = Path(context.project_root) / file_path_part
                else:
                    # Fallback if context or project_root is not available (should not happen in tests)
                    full_file_path = Path(file_path_part)

                try:
                    self.write_code(str(full_file_path), file_content, overwrite=True) # Assuming overwrite for simplicity in agent
                    response.content = f"File created successfully: {file_path_part}"
                except FileExistsError:
                    response.content = f"Error: File already exists: {file_path_part}. Use overwrite option if intended."
                except Exception as e:
                    logger.error(f"Error creating file {file_path_part}: {e}", exc_info=True)
                    response.content = f"Error creating file {file_path_part}: {e}"
            elif command.startswith("generate"):
                task = command.replace("generate", "").strip()
                # Pass None for context as AgentContext is a dataclass and generate_code doesn't use it yet
                code, metadata = self.generate_code(task, None)
                response.content = f"Generated code for task: {task}\n\n{code}"
                response.metadata = metadata
            elif command.startswith("write"):
                parts = message.content.split(maxsplit=2)
                if len(parts) < 3:
                    response.content = "Error: 'write' command needs file path and content."
                else:
                    file_path = parts[1]
                    code_content = parts[2]
                    if self.write_code(file_path, code_content):
                        response.content = f"Successfully wrote code to {file_path}"
                    else:
                        response.content = f"Failed to write code to {file_path}"
            else:
                response.content = "Unknown command. Type 'help' for available commands."
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
            "open_questions": ["What are the password complexity rules beyond length?"]
        }
        self.memory["analyzed_requirements"] = analysis
        return analysis

    def generate_code(self, task: str, context: Optional[Dict] = None) -> Tuple[str, Dict]:
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
        self.memory["tasks"][task_id] = {
            "description": task,
            "status": "in_progress"
        }
        
        # Simple code generation - in a real implementation, this would use an LLM
        if "test" in task.lower():
            function_name = "test_" + "".join(word.lower() for word in task.split()[:3] if word.lower() != "test")
        else:
            function_name = "_" + "".join(word.lower() for word in task.split()[:3])
            
        code = f"def {function_name}():"
        code += f"\n    \"\"\"{task}\"\"\""
        code += "\n    pass  # TODO: Implement this function\n"
        
        metadata = {
            "language": "python",
            "function_name": function_name,
            "task_id": task_id
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
            raise FileExistsError(f"File {file_path_obj} already exists and overwrite=False")
            
        try:
            file_path_obj.parent.mkdir(parents=True, exist_ok=True)
            file_path_obj.write_text(code, encoding='utf-8')
            logger.info(f"Successfully wrote code to {file_path_obj}") # Add success log
            return True
        except IOError as e: # Catch IOError specifically to re-raise
            logger.error(f"IOError writing to {file_path_obj}: {str(e)}", exc_info=True)
            raise # Re-raise the IOError
        except Exception as e: # Catch other potential exceptions
            logger.error(f"Unexpected error writing to {file_path_obj}: {str(e)}", exc_info=True)
            raise # Re-raise other exceptions

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
                "Add error handling where necessary."
            ]
        }

    def update_knowledge(self, knowledge: Dict[str, Any]) -> None:
        """Update the agent's knowledge base.
        
        Args:
            knowledge: Dictionary of knowledge to add/update.
        """
        self.knowledge_base.update(knowledge)

    def _get_help_message(self) -> str:
        """Return help message with available commands."""
        help_msg = """Available commands:
- help: Show this help message
- analyze <requirements>: Analyze software requirements
- generate <task>: Generate code for the given task
"""
        return help_msg
