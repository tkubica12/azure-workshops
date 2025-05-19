# ============================
# Stage 1: Builder (install dependencies)
# ============================
# Using the official uv image with Python 3.14 on Bookworm Slim (Debian)
FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim AS builder

 # Set working directory
WORKDIR /app

 # Copy lock and project file for dependency installation
COPY uv.lock pyproject.toml /app/

 # Set environment variables for faster and more stable installation
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

 # Use cache for uv so dependencies are not installed from scratch on every build
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project

 # ============================
# Stage 2: Build application
# ============================
# Copy the rest of the code and install the project itself
COPY . /app

 # Sync again, this time with project installation
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

 # ============================
# Stage 3: Runtime (final image)
# ============================
# We could use a smaller image like python-slim or alpine, but here we stick with Debian
FROM python:3.12-bookworm-slim AS runtime

 # Copy virtual environment and code from builder stage
COPY --from=builder /app /app

 # Adjust PATH to run python/uvicorn from the created .venv
ENV PATH="/app/.venv/bin:${PATH}"

 # Set working directory
WORKDIR /app

EXPOSE 8000

ENTRYPOINT ["uv", "run", "python", "main.py"]
