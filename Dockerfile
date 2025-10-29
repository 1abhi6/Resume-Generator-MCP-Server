# syntax=docker/dockerfile:1
# Use official uv image with Python preinstalled
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

# Set working directory
WORKDIR /app

# Copy all files into the container
COPY . /app

# Install LibreOffice and required fonts
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libreoffice \
        libreoffice-writer \
        libreoffice-calc \
        libreoffice-impress \
        fonts-dejavu-core && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies using uv (reads pyproject.toml + uv.lock)
RUN uv sync --frozen

# Expose port for FastMCP / FastAPI
EXPOSE 8000

# Start your MCP server (adjust filename if needed)
CMD ["uv", "run", "main.py"]
