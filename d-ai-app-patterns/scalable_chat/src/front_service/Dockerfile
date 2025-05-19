FROM python:3.12-slim

WORKDIR /app

# Install curl for the uv installer
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# Download and install uv
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Copy dependency files and install dependencies
COPY pyproject.toml uv.lock ./
RUN uv pip install

# Copy the rest of the project
COPY . .

EXPOSE 8000

CMD ["uv", "run", "main.py"]