# Dockerfile for the Locust test client

# 1. Use an official Python runtime as a parent image
FROM python:3.12-slim

# 2. Install uv (Python package manager from Astral)
# Ensure you use a version of uv that is suitable or pin it.
# Check https://github.com/astral-sh/uv for the latest installation method or versions.
ARG UV_VERSION=0.1.40 
RUN apt-get update && apt-get install -y curl --no-install-recommends && \
    curl -LsSf https://astral.sh/uv/install.sh | sh && \
    mv /root/.cargo/bin/uv /usr/local/bin/uv && \
    apt-get remove -y curl && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# 3. Set the working directory in the container
WORKDIR /app

# 4. Copy the dependencies file and install dependencies using uv
COPY requirements.txt .
# Using --system because we are in a controlled container environment.
# --no-cache to reduce layer size.
RUN uv pip install --no-cache --system -r requirements.txt

# 5. Copy the Locust test script (main.py)
COPY main.py .

# 6. Expose the default Locust web UI port
EXPOSE 8089

# 7. Define the entrypoint and default command
# This allows users to append locust arguments directly to `docker run`
# e.g., docker run <image_name> --headless --users 10 --spawn-rate 1
# The main.py script will load TARGET_BASE_URL from environment variables.
ENTRYPOINT ["locust"]
CMD ["-f", "main.py"]