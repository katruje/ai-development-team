from setuptools import setup, find_packages

setup(
    name="ai-development-team",
    version="0.1.0",
    packages=find_packages(include=["agent_core*", "workflows*", "services*", "interfaces*", "config*"]),
    install_requires=[
        "typer>=0.9.0",
        "rich>=13.0.0",
        "pydantic>=2.0.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pre-commit>=3.0.0",
        ]
    },
    python_requires=">=3.9",
)
