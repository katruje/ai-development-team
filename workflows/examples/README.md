# Hello World Workflow

This workflow generates a simple "Hello, World!" Python package with a complete project structure, tests, and documentation.

## Features

- Creates a well-structured Python package
- Sets up testing with pytest
- Configures code formatting with black and isort
- Generates a proper `pyproject.toml`
- Creates a comprehensive README
- Initializes a git repository
- Runs tests to verify the generated code

## Usage

### Prerequisites

- Python 3.9+
- pip

### Running the Workflow

1. Navigate to the project root:
   ```bash
   cd /path/to/ai_development_team
   ```

2. Run the workflow:
   ```bash
   python -m workflows.hello_world --output my_hello_world
   ```

   This will create a new directory called `my_hello_world` with the generated project.

### Command Line Options

- `--config`: Path to the workflow configuration file (default: `config.yaml` in the workflow directory)
- `--output`: Output directory for the generated project (default: `hello_world`)

## Project Structure

The generated project will have the following structure:

```
my_hello_world/
├── src/
│   └── my_hello_world/
│       ├── __init__.py
│       └── main.py
├── tests/
│   └── test_hello_world.py
├── pyproject.toml
└── README.md
```

## Customization

### Configuration

You can customize the workflow by editing the `config.yaml` file in the workflow directory. The configuration includes:

- Project metadata (name, version, description, etc.)
- Author information
- Python version requirements
- Dependencies
- Workflow steps

### Templates

Templates are stored in the `templates` directory and use the Jinja2 templating engine. You can modify these templates to customize the generated files.

## Development

### Running Tests

To run the tests for the workflow itself:

```bash
pytest workflows/hello_world/tests/
```

### Adding New Templates

1. Create a new template file in the `templates` directory with a `.j2` extension
2. Add a new step to the workflow in `config.yaml` that uses the template
3. The template will have access to all variables in the `context` section of the config

## License

MIT
