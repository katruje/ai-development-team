# Code Generator Module

## Overview
The Code Generator module provides a flexible and extensible way to generate code programmatically. It's designed to support the AI Development Team's needs for dynamic code generation based on templates and structured definitions.

## Features

- **CodeArtifact Class**: Represents generated code with metadata
- **Template-based Generation**: Generate code from templates with variable substitution
- **Programmatic Generation**: Build code using Python objects and methods
- **File System Integration**: Save generated code to disk with proper directory structure
- **Extensible**: Support for multiple programming languages and custom templates

## Installation

The code generator is included in the core module of the AI Development Team package.

## Basic Usage

### Creating a Simple Module

```python
from ai_development_team.core import CodeGenerator

# Initialize the generator
generator = CodeGenerator()

# Generate a basic module
module = generator.generate_module(
    module_name="calculator",
    docstring="A simple calculator module.",
    imports=["typing"],
    functions=[
        {
            "name": "add",
            "params": ["a: float", "b: float"],
            "docstring": "Add two numbers.",
            "body": ["return a + b"],
            "return_type": "float"
        },
        {
            "name": "multiply",
            "params": ["a: float", "b: float"],
            "docstring": "Multiply two numbers.",
            "body": ["return a * b"],
            "return_type": "float"
        }
    ]
)

# Save to disk
module.save("src")
```

### Using Templates

1. Create a template file (e.g., `templates/python/class.j2`):
   ```python
   class {{ class_name }}:
       """{{ docstring }}"""
       
       def __init__(self{{ ', '.join([''] + constructor_params) if constructor_params else '' }}):
           {% for param in constructor_params %}
           self.{{ param.split('=')[0].strip() }} = {{ param.split('=')[0].strip() }}
           {% endfor %}
   ```

2. Use the template:
   ```python
   generator = CodeGenerator("templates")
   
   result = generator.generate_from_template(
       template_name="python.class",
       context={
           "class_name": "Person",
           "docstring": "Represents a person.",
           "constructor_params": ["name: str", "age: int = 30"]
       },
       name="Person"
   )
   
   result.save("src/models")
   ```

## API Reference

### `CodeArtifact` Class

Represents a piece of generated code with associated metadata.

#### Attributes
- `name` (str): Name of the artifact
- `content` (str): The generated code content
- `artifact_type` (str): Type of artifact (e.g., 'module', 'class', 'test')
- `language` (str): Programming language (default: 'python')
- `metadata` (dict): Additional metadata about the artifact

#### Methods
- `save(base_path)`: Save the artifact to the specified base directory
- `get_file_path()`: Get the appropriate file path for this artifact

### `CodeGenerator` Class

Generates code based on templates and programmatic definitions.

#### Methods
- `generate_module(module_name, imports=None, functions=None, classes=None, **kwargs)`: Generate a Python module
- `generate_from_template(template_name, context=None, output_path=None, **kwargs)`: Generate code from a template
- `_generate_class(class_def)`: (Internal) Generate a class definition
- `_generate_function(func_def)`: (Internal) Generate a function definition
- `_load_templates()`: (Internal) Load templates from the templates directory

## Advanced Usage

### Custom Template Loaders

You can extend the generator to load templates from different sources:

```python
class DatabaseTemplateLoader(CodeGenerator):
    def _load_templates(self):
        # Load templates from a database
        templates = db.query("SELECT name, content FROM templates")
        self._templates = {t.name: t.content for t in templates}
```

### Custom Artifact Types

Extend `CodeArtifact` to support custom artifact types:

```python
class WebComponentArtifact(CodeArtifact):
    def get_file_path(self):
        return Path("web_components") / f"{self.name}.jsx"
```

## Best Practices

1. **Template Organization**: Organize templates by language and component type
2. **Testing**: Always test generated code, especially when using templates
3. **Version Control**: Consider checking in template files for better maintainability
4. **Documentation**: Document template variables and expected context
5. **Error Handling**: Add validation for template variables and context

## Examples

See the `examples/` directory for complete examples of using the code generator.

## Contributing

Contributions are welcome! Please follow the project's coding standards and submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
