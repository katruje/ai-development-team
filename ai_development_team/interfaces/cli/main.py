"""
Command Line Interface for the AI Development Team.

This module provides a CLI for interacting with the AI Development Team
functionality, allowing users to manage projects and development workflows.
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import Optional

from ai_development_team.core.project import Project
from ai_development_team.core.workflow import DevelopmentWorkflow

def setup_logging(verbose: bool = False) -> None:
    """
    Configure logging for the CLI.
    
    Args:
        verbose: If True, enable debug logging
    """
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

def parse_args() -> argparse.Namespace:
    """
    Parse command line arguments.
    
    Returns:
        Parsed command line arguments
    """
    parser = argparse.ArgumentParser(
        description="AI Development Team - Automate software development with AI agents"
    )
    
    # Global arguments
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    # Subcommands
    subparsers = parser.add_subparsers(dest='command', required=True)
    
    # Project commands
    project_parser = subparsers.add_parser('project', help='Project management commands')
    project_subparsers = project_parser.add_subparsers(dest='project_command', required=True)
    
    # Project create
    create_parser = project_subparsers.add_parser('create', help='Create a new project')
    create_parser.add_argument('name', help='Project name')
    create_parser.add_argument('-d', '--description', help='Project description', default='')
    create_parser.add_argument('--dir', help='Project directory', default='.')
    
    # Workflow commands
    workflow_parser = subparsers.add_parser('workflow', help='Workflow management commands')
    workflow_subparsers = workflow_parser.add_subparsers(dest='workflow_command', required=True)
    
    # Workflow start
    start_parser = workflow_subparsers.add_parser('start', help='Start a development workflow')
    start_parser.add_argument('project_dir', help='Project directory')
    
    # Workflow analyze
    analyze_parser = workflow_subparsers.add_parser('analyze', help='Analyze project requirements')
    analyze_parser.add_argument('project_dir', help='Project directory')
    
    # Workflow design
    design_parser = workflow_subparsers.add_parser('design', help='Generate system design')
    design_parser.add_argument('project_dir', help='Project directory')
    
    return parser.parse_args()

def create_project(args: argparse.Namespace) -> int:
    """
    Create a new project.
    
    Args:
        args: Command line arguments
        
    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    try:
        project = Project(
            name=args.name,
            description=args.description,
            directory=Path(args.dir) / args.name
        )
        
        if project.initialize():
            print(f"✅ Created project '{project.name}' at {project.directory}")
            return 0
        else:
            print(f"❌ Failed to create project '{args.name}'", file=sys.stderr)
            return 1
            
    except Exception as e:
        print(f"❌ Error creating project: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1

def start_workflow(args: argparse.Namespace) -> int:
    """
    Start a development workflow.
    
    Args:
        args: Command line arguments
        
    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    try:
        project_dir = Path(args.project_dir).absolute()
        project = Project(
            name=project_dir.name,
            directory=project_dir
        )
        
        workflow = DevelopmentWorkflow(project=project)
        if workflow.start():
            print(f"✅ Started development workflow for project at {project_dir}")
            return 0
        else:
            print("❌ Failed to start workflow", file=sys.stderr)
            return 1
            
    except Exception as e:
        print(f"❌ Error starting workflow: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1

def analyze_requirements(args: argparse.Namespace) -> int:
    """
    Analyze project requirements.
    
    Args:
        args: Command line arguments
        
    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    try:
        project_dir = Path(args.project_dir).absolute()
        project = Project(
            name=project_dir.name,
            directory=project_dir
        )
        
        workflow = DevelopmentWorkflow(project=project)
        analysis = workflow.analyze_requirements()
        
        print("\n📋 Requirements Analysis Results:")
        print(f"- Status: {analysis.get('status', 'unknown')}")
        if 'requirements' in analysis:
            print("\nRequirements:")
            print(analysis['requirements'])
            
        return 0
        
    except Exception as e:
        print(f"❌ Error analyzing requirements: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1

def generate_design(args: argparse.Namespace) -> int:
    """
    Generate system design.
    
    Args:
        args: Command line arguments
        
    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    try:
        project_dir = Path(args.project_dir).absolute()
        project = Project(
            name=project_dir.name,
            directory=project_dir
        )
        
        workflow = DevelopmentWorkflow(project=project)
        design = workflow.generate_design()
        
        print("\n🏗️  System Design:")
        print(f"- Architecture: {design.get('architecture', 'N/A')}")
        print("\nComponents:")
        for component in design.get('components', []):
            print(f"  - {component}")
        print("\nTechnologies:")
        for tech in design.get('technologies', []):
            print(f"  - {tech}")
            
        return 0
        
    except Exception as e:
        print(f"❌ Error generating design: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1

def main() -> int:
    """
    Main entry point for the CLI.
    
    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    args = parse_args()
    setup_logging(args.verbose)
    
    # Route to appropriate command handler
    if args.command == 'project':
        if args.project_command == 'create':
            return create_project(args)
    elif args.command == 'workflow':
        if args.workflow_command == 'start':
            return start_workflow(args)
        elif args.workflow_command == 'analyze':
            return analyze_requirements(args)
        elif args.workflow_command == 'design':
            return generate_design(args)
    
    print(f"Unknown command: {args.command}", file=sys.stderr)
    return 1

if __name__ == "__main__":
    sys.exit(main())
