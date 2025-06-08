# Stage 1: Builder
FROM python:3.12-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:0.4.9 /uv /usr/local/bin/uv
WORKDIR /app
COPY uv.lock pyproject.toml /app/
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

# Stage 2: Runtime
FROM python:3.12-slim AS runtime
COPY --from=builder /app /app
COPY --from=builder /usr/local/bin/uv /usr/local/bin/uv
ENV PATH="/app/.venv/bin:${PATH}"
WORKDIR /app
EXPOSE 8003
ENTRYPOINT ["uv", "run", "python", "main.py"]
