# Use the official Python image as the base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONPATH=/app

# Create a non-root user and switch to it
RUN adduser --disabled-password --gecos "" developer && \
    mkdir /app && \
    chown developer:developer /app

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy only the necessary files for dependency installation first
COPY pyproject.toml setup.py README.md ./
COPY requirements.txt .

# Install Python dependencies
RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir -r requirements.txt && \
    python3 -m pip install --no-cache-dir -e ".[dev]"

# Copy the rest of the application code
COPY . .

# Change ownership of the application code to the non-root user
RUN chown -R developer:developer /app

# Configure Python command consistency
RUN echo 'alias python=python3' >> /home/developer/.bashrc && \
    echo 'export PYTHONPATH=/app' >> /home/developer/.bashrc

# Switch to the non-root user
USER developer

# Set the default command to run the application
CMD ["python3", "-m", "interfaces.cli.main", "start"]
