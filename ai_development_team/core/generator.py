"""
Code Generator Module.

This module provides functionality for generating code based on templates and requirements.
It supports generating different types of code artifacts like modules, classes, and functions.
"""

import os
import re
import logging
from pathlib import Path
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass, field
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class CodeArtifact:
    """Represents a code artifact with its content and metadata."""
    
    name: str
    content: str
    artifact_type: str  # e.g., 'module', 'class', 'function', 'test'
    language: str = 'python'
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Initialize the code artifact with default metadata."""
        self.metadata.setdefault('created_at', datetime.utcnow().isoformat())
        self.metadata.setdefault('generator', 'CodeGenerator')
    
    def save(self, base_path: Union[str, Path] = '.') -> Path:
        """Save the code artifact to disk.
        
        Args:
            base_path: Base directory to save the artifact
            
        Returns:
            Path to the saved file
        """
        path = Path(base_path) / self.get_file_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.content, encoding='utf-8')
        logger.info("Saved %s to %s", self.artifact_type, path)
        return path
    
    def get_file_path(self) -> Path:
        """Get the file path for this artifact."""
        if self.artifact_type == 'module':
            return Path(self.name.replace('.', '/') + '.py')
        elif self.artifact_type == 'test':
            return Path('tests') / f'test_{self.name}.py'
        return Path(self.name + '.py')


class CodeGenerator:
    """Generates code based on templates and requirements."""
    
    def __init__(self, templates_dir: Optional[Union[str, Path]] = None):
        """Initialize the code generator with optional templates directory.
        
        Args:
            templates_dir: Directory containing code templates
        """
        self.templates_dir = Path(templates_dir) if templates_dir else None
        self._templates = {}
        self._load_templates()
    
    def _load_templates(self) -> None:
        """Load templates from the templates directory if it exists."""
        if not self.templates_dir or not self.templates_dir.exists():
            logger.debug("No templates directory found at %s", self.templates_dir)
            return
            
        for template_file in self.templates_dir.glob('**/*.j2'):
            rel_path = template_file.relative_to(self.templates_dir)
            template_name = str(rel_path.with_suffix('')).replace(os.sep, '.')
            try:
                with open(template_file, 'r', encoding='utf-8') as f:
                    self._templates[template_name] = f.read()
                logger.debug("Loaded template: %s", template_name)
            except Exception as e:
                logger.warning("Failed to load template %s: %s", template_file, e)
    
    def generate_module(
        self, 
        module_name: str, 
        imports: Optional[List[str]] = None,
        functions: Optional[List[Dict]] = None,
        classes: Optional[List[Dict]] = None,
        docstring: Optional[str] = None,
        **kwargs
    ) -> CodeArtifact:
        """Generate a Python module.
        
        Args:
            module_name: Name of the module (can include package path)
            imports: List of import statements
            functions: List of function definitions
            classes: List of class definitions
            docstring: Module docstring
            **kwargs: Additional metadata
            
        Returns:
            CodeArtifact containing the generated module
        """
        imports = imports or []
        functions = functions or []
        classes = classes or []
        
        # Generate module content
        lines = []
        
        # Shebang
        lines.append('#!/usr/bin/env python3')
        lines.append('"""')
        lines.append(docstring or f"{module_name} module.")
        lines.append('"""')
        lines.append('')
        
        # Imports
        if imports:
            for imp in sorted(set(imports)):  # Remove duplicates and sort
                lines.append(f"import {imp}")
            lines.append('')
        
        # Classes
        for class_def in classes:
            lines.extend(self._generate_class(class_def))
            lines.append('')
        
        # Functions
        for func_def in functions:
            lines.extend(self._generate_function(func_def))
            lines.append('')
        
        # Remove trailing newlines
        content = '\n'.join(lines).strip() + '\n'
        
        return CodeArtifact(
            name=module_name,
            content=content,
            artifact_type='module',
            metadata={
                'generator': self.__class__.__name__,
                'timestamp': datetime.utcnow().isoformat(),
                **kwargs
            }
        )
    
    def _generate_class(self, class_def: Dict) -> List[str]:
        """Generate a class definition."""
        lines = []
        
        # Class docstring
        if 'docstring' in class_def:
            lines.append(f'class {class_def["name"]}:')
            lines.append('    """' + class_def['docstring'] + '"""')
        else:
            lines.append(f'class {class_def["name"]}:')
            lines.append('    pass')
        
        return lines
    
    def _generate_function(self, func_def: Dict) -> List[str]:
        """Generate a function definition."""
        lines = []
        
        # Function signature
        params = ', '.join(func_def.get('params', []))
        signature = f'def {func_def["name"]}({params})'
        
        # Return type hint
        if 'return_type' in func_def:
            signature += f' -> {func_def["return_type"]}'
        
        lines.append(signature + ':')
        
        # Function docstring
        if 'docstring' in func_def:
            lines.append('    """' + func_def['docstring'] + '"""')
        
        # Function body
        if 'body' in func_def:
            for line in func_def['body']:
                lines.append(f'    {line}')
        else:
            lines.append('    pass')
        
        return lines
    
    def generate_from_template(
        self, 
        template_name: str, 
        context: Optional[Dict] = None,
        output_path: Optional[Union[str, Path]] = None,
        **kwargs
    ) -> CodeArtifact:
        """Generate code from a template.
        
        Args:
            template_name: Name of the template to use
            context: Variables to pass to the template
            output_path: Path to save the generated code (optional)
            **kwargs: Additional metadata
            
        Returns:
            CodeArtifact containing the generated code
        """
        context = context or {}
        
        # Get template content
        if template_name in self._templates:
            template = self._templates[template_name]
        else:
            raise ValueError(f"Template '{template_name}' not found")
        
        # Simple template rendering (for now, could be extended with Jinja2)
        content = template
        for key, value in context.items():
            content = content.replace(f'{{{{ {key} }}}}', str(value))
        
        artifact = CodeArtifact(
            name=kwargs.get('name', template_name.split('.')[-1]),
            content=content,
            artifact_type=kwargs.get('artifact_type', 'file'),
            metadata={
                'template': template_name,
                'generated_at': datetime.utcnow().isoformat(),
                **kwargs
            }
        )
        
        if output_path:
            artifact.save(output_path)
            
        return artifact
