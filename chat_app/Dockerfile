FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt /app/metagpt-requirements.txt
COPY chat_app/requirements-api.txt /app/requirements-api.txt

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/metagpt-requirements.txt
RUN pip install --no-cache-dir -r /app/requirements-api.txt

# Copy MetaGPT source code only (config will be mounted as volume)
COPY metagpt /app/metagpt

# Copy chat app
COPY chat_app /app/chat_app

# Create config directory for volume mount
RUN mkdir -p /app/config

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV METAGPT_PROJECT_ROOT=/app

# Expose port
EXPOSE 8001

# Change to chat_app directory
WORKDIR /app/chat_app

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
