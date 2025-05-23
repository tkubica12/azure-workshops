# Scalable Chat - Locust Load Test Client

This directory contains a Locust load test client for the Scalable Chat application.
It simulates multiple users concurrently starting sessions, sending chat messages, and receiving Server-Sent Events (SSE) streams.

## Prerequisites

- Python 3.8+
- `uv` Python package manager (recommended for managing the virtual environment and dependencies)

## Setup

1.  **Navigate to this directory:**
    ```powershell
    cd c:\git\azure-workshops\d-ai-app-patterns\scalable_chat\src\test_client
    ```

2.  **Create and configure your `.env` file:**
    Copy the example environment file and customize it with your settings.
    ```powershell
    Copy-Item .env.example .env
    ```
    Edit the `.env` file:
    - `TARGET_BASE_URL`: **Required.** Set this to the base URL of your running front service (e.g., `http://localhost:8000` or your deployed service URL).
    - `LOCUST_USERS`: Number of concurrent users to simulate (default used by `main.py` if not set for CLI, but best to set for headless).
    - `LOCUST_SPAWN_RATE`: Number of users to spawn per second.
    - `LOCUST_RUN_TIME`: Duration for the test to run (e.g., `60s`, `1m30s`). Only used for headless mode.
    - `TEST_MESSAGE` (Optional): A specific message to send in the chat; if not set, a default message will be used.

3.  **Install dependencies using `uv`:**
    This will create a virtual environment (if one doesn't exist) and install `locust`, `python-dotenv`, and `sseclient-py`.
    ```powershell
    uv pip install -r requirements.txt
    ```

## Running the Load Tests

You can run the Locust tests in headless mode (for CI/automated runs) or with the Locust Web UI (for interactive testing and real-time results).

### 1. Headless Mode

This mode is suitable for automated testing. It runs for a specified duration and then exits.
Ensure `LOCUST_USERS`, `LOCUST_SPAWN_RATE`, and `LOCUST_RUN_TIME` are set in your `.env` file or passed as environment variables to your shell.

```powershell
# Ensure environment variables are loaded or pass them directly
# Example assuming they are set in your current shell session (e.g., from .env or manually)
uv run -- locust -f main.py --headless --users $env:LOCUST_USERS --spawn-rate $env:LOCUST_SPAWN_RATE --run-time $env:LOCUST_RUN_TIME --host $env:TARGET_BASE_URL

# Alternatively, pass values directly:
uv run -- locust -f main.py --headless --users 50 --spawn-rate 10 --run-time 3m --host http://localhost:8000 --only-summary
```
Locust will print statistics to the console upon completion.

### 2. Web UI Mode

This mode provides a web interface to control the test and view live statistics.

```powershell
uv run -- locust -f main.py
```

Once Locust starts, open your web browser and navigate to `http://localhost:8089` (or the port indicated in the console output).
In the Web UI:
- Enter the "Number of users" (e.g., 10).
- Enter the "Spawn rate" (users to start per second, e.g., 1).
- Enter the "Host" (this should be pre-filled by `TARGET_BASE_URL` from your `.env` file, e.g., `http://localhost:8000`).
- Click "Start swarming".

You can monitor various charts and statistics in real-time, and stop the test when desired.

## Test File

- `main.py`: Contains the Locust test script defining user behavior.
- `.env.example`: Example environment configuration.