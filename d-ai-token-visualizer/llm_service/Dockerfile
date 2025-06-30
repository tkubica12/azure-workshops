# Dockerfile for Local LLM Service
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies and uv
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && curl -LsSf https://astral.sh/uv/install.sh | sh

# Add uv to PATH
ENV PATH="/root/.cargo/bin:$PATH"

# Copy project files
COPY pyproject.toml uv.lock* ./

# Install Python dependencies using uv
RUN uv sync --frozen --no-dev

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8001

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8001/health || exit 1

# Run the application using uv
CMD ["uv", "run", "main.py"]
