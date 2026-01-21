# Stage 1: Build Frontend
FROM node:20-slim AS frontend-builder
WORKDIR /app/frontend
COPY chat_app/frontend/package*.json ./
RUN npm install
COPY chat_app/frontend/ ./
RUN npm run build

# Stage 2: Backend & Runtime
FROM python:3.12-slim

# Install minimal system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
COPY chat_app/requirements-api.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -r requirements-api.txt

# Copy MetaGPT source and install in editable mode
COPY . .
RUN pip install -e .

# Copy built frontend to FastAPI static directory
RUN mkdir -p /app/chat_app/static
COPY --from=frontend-builder /app/frontend/dist /app/chat_app/static

# Environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV METAGPT_PROJECT_ROOT=/app

# Expose port
EXPOSE 8001

# Change to chat_app directory
WORKDIR /app/chat_app

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
