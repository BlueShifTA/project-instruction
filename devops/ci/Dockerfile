# Dockerfile for the project template

# Use Python 3.13 slim image as base
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:${PATH}"

# Copy project files
COPY ../../pyproject.toml .
COPY ../../projects/ ./projects/
COPY ../../docs/ ./docs/
COPY ../../README.md .

# Install Python dependencies
RUN uv venv && \
    . .venv/bin/activate && \
    uv pip install -e . && \
    uv sync --all-packages --all-groups

# Set the entrypoint to use the virtual environment
ENV PATH="/app/.venv/bin:${PATH}"

# Default command
CMD ["python", "--version"]
