#!/bin/bash

# Exit on error
set -e

# Function to check if a command exists
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

# Check if Docker is installed
if ! command_exists docker; then
  echo "Docker is not installed. Please install Docker and try again."
  exit 1
fi

# Check if docker-compose is installed
if ! command_exists docker-compose; then
  echo "docker-compose is not installed. Please install docker-compose and try again."
  exit 1
fi

# Build and start the containers
echo "Building and starting the AI Development Team container..."
docker-compose up -d --build

# Check if the container is running
if [ "$(docker ps -q -f name=ai-dev-team)" ]; then
  echo "\n✅ AI Development Team container is running!"
  echo "\nYou can now access the container with:"
  echo "  docker-compose exec ai-dev-team bash"
  echo "\nOr run a command directly:"
  echo "  docker-compose exec ai-dev-team python -m interfaces.cli.main --help"
  echo "\nTo view logs:"
  echo "  docker-compose logs -f"
  echo "\nTo stop the container:"
  echo "  docker-compose down"
else
  echo "\n❌ Failed to start the container. Check the logs with:"
  echo "  docker-compose logs"
  exit 1
fi
