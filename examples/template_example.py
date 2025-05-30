"""
Template-based code generation example.

This example demonstrates how to use the CodeGenerator with custom templates
for generating code.
"""

import sys
from pathlib import Path
from ai_development_team.core import CodeGenerator

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))


def setup_templates():
    """Set up example templates in a temporary directory."""
    templates_dir = Path("example_templates")
    templates_dir.mkdir(exist_ok=True)

    # Create a simple class template
    class_template = """class {{ class_name }}({{ base_class }}):
    \"\"\"{{ docstring }}\"\"\"

    def __init__(self{{
        ', '.join([''] + constructor_params) if constructor_params else ''
    }}):
        {% for param in constructor_params %}
        self.{{ param.split('=')[0].strip() }} = {{ param.split('=')[0].strip() }}
        {% endfor %}

    {% for method in methods %}
    def {{ method.name }}(self
            {%- for param in method.params %}, {{ param }}{% endfor %}):
        \"\"\"{{ method.docstring }}\"\"\"
        {% if method.body %}
        {% for line in method.body %}
        {{ line }}
        {% endfor %}
        {% else %}
        pass
        {% endif %}

    {% endfor %}
"""

    # Create templates directory structure
    (templates_dir / "python").mkdir(exist_ok=True)

    # Save the template
    with open(templates_dir / "python" / "class.j2", "w") as f:
        f.write(class_template)

    return templates_dir


def main():
    # Set up example templates
    templates_dir = setup_templates()

    # Initialize the generator with our templates
    generator = CodeGenerator(templates_dir)

    # Generate a class using the template
    person_class = generator.generate_from_template(
        template_name="python.class",
        context={
            "class_name": "Person",
            "base_class": "object",
            "docstring": "Represents a person with name and age.",
            "constructor_params": ["name: str", "age: int = 0"],
            "methods": [
                {
                    "name": "greet",
                    "params": ["greeting: str = 'Hello'"],
                    "docstring": "Return a greeting message.",
                    "body": [
                        "return (",
                        "f'{greeting}, my name is {self.name} ",
                        "and I am {self.age} years old.'",
                        ")",
                    ],
                },
                {
                    "name": "have_birthday",
                    "params": [],
                    "docstring": (
                        "Increment the person's age by 1."
                    ),
                    "body": ["self.age += 1", "return self.age"],
                },
            ],
        },
        name="Person",
    )

    # Save the generated class
    output_dir = Path("generated")
    person_class.save(output_dir)
    print(f"Generated Person class at: {output_dir / person_class.get_file_path()}")

    # Print the generated code
    print("\nGenerated code:")
    print("-" * 80)
    print(person_class.content)
    print("-" * 80)

    # Clean up (in a real app, you'd keep your templates)
    import shutil

    shutil.rmtree(templates_dir)


if __name__ == "__main__":
    main()
