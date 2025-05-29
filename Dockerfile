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
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -e ".[dev]"

# Copy the rest of the application code
COPY . .

# Change ownership of the application code to the non-root user
RUN chown -R developer:developer /app

# Switch to the non-root user
USER developer

# Set the default command to run the application
CMD ["python", "-m", "interfaces.cli.main", "start"]
