FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy all necessary files
COPY villager_server.py /app/villager_server.py
COPY villager_visuals.py /app/villager_visuals.py
COPY config.py /app/config.py
COPY github_tools.py /app/github_tools.py
COPY github_tool_discovery.py /app/github_tool_discovery.py
COPY mcp/ /app/mcp/

# Install required packages
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    mcp \
    requests \
    pydantic \
    python-multipart \
    pygithub \
    python-dotenv

# Create necessary directories
RUN mkdir -p /app/logs /app/data

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV VILLAGER_HOST=0.0.0.0
ENV VILLAGER_PORT=37695

EXPOSE 37695

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:37695/api/status || exit 1

ENTRYPOINT ["python", "-u", "/app/mcp/serve_all.py"]

