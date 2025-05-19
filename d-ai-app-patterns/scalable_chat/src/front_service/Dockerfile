# Use official Python image
FROM python:3.12-slim

# Set work directory
WORKDIR /app

# Install dependencies via pip-compatible uv
COPY pyproject.toml uv.lock ./
RUN pip install --upgrade pip \
    && pip install uv \
    && uv install

# Copy project files
COPY . .

# Expose port
EXPOSE 8000

# Start the app with uvicorn
CMD ["uv", "run", "main.py"]
