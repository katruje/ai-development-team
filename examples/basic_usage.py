"""
Basic usage example for the CodeGenerator.

This example demonstrates how to use the CodeGenerator to create a simple
Python module with functions and classes.
"""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ai_development_team.core import CodeGenerator

def main():
    # Initialize the generator
    generator = CodeGenerator()
    
    # Generate a calculator module
    calculator = generator.generate_module(
        module_name="calculator",
        docstring="""
        A simple calculator module.
        
        This module provides basic arithmetic operations.
        """,
        imports=["typing", "math"],
        functions=[
            {
                "name": "add",
                "params": ["a: float", "b: float"],
                "docstring": "Add two numbers.",
                "body": ["return a + b"],
                "return_type": "float"
            },
            {
                "name": "subtract",
                "params": ["a: float", "b: float"],
                "docstring": "Subtract b from a.",
                "body": ["return a - b"],
                "return_type": "float"
            },
            {
                "name": "multiply",
                "params": ["a: float", "b: float"],
                "docstring": "Multiply two numbers.",
                "body": ["return a * b"],
                "return_type": "float"
            },
            {
                "name": "divide",
                "params": ["a: float", "b: float"],
                "docstring": "Divide a by b.",
                "body": [
                    "if b == 0:",
                    "    raise ValueError('Cannot divide by zero')",
                    "return a / b"
                ],
                "return_type": "float"
            },
            {
                "name": "is_prime",
                "params": ["n: int"],
                "docstring": "Check if a number is prime.",
                "body": [
                    "if n < 2:",
                    "    return False",
                    "for i in range(2, int(math.sqrt(n)) + 1):",
                    "    if n % i == 0:",
                    "        return False",
                    "return True"
                ],
                "return_type": "bool"
            }
        ],
        classes=[
            {
                "name": "Calculator",
                "docstring": "A simple calculator class.",
                "methods": [
                    {
                        "name": "__init__",
                        "params": ["self", "initial_value: float = 0"],
                        "docstring": "Initialize the calculator with an optional initial value.",
                        "body": ["self.value = initial_value"]
                    },
                    {
                        "name": "add",
                        "params": ["self", "x: float"],
                        "docstring": "Add a value to the current result.",
                        "body": ["self.value += x", "return self"],
                        "return_type": "'Calculator'"
                    },
                    {
                        "name": "get_value",
                        "params": ["self"],
                        "docstring": "Get the current result.",
                        "body": ["return self.value"],
                        "return_type": "float"
                    },
                    {
                        "name": "reset",
                        "params": ["self"],
                        "docstring": "Reset the calculator to zero.",
                        "body": ["self.value = 0", "return self"],
                        "return_type": "'Calculator'"
                    }
                ]
            }
        ]
    )
    
    # Save the generated module
    output_dir = Path("generated")
    calculator.save(output_dir)
    print(f"Generated calculator module at: {output_dir / calculator.get_file_path()}")
    
    # Print the generated code
    print("\nGenerated code:")
    print("-" * 80)
    print(calculator.content)
    print("-" * 80)

if __name__ == "__main__":
    main()
