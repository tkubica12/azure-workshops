# SSE Service

This service handles Server-Sent Events (SSE) streaming for the scalable chat application. It's responsible for receiving tokens from the message queue and streaming them to connected clients.

## Features

- **Session-aware streaming**: Uses Service Bus sessions to receive tokens for specific chat sessions
- **Message filtering**: Filters tokens by `chatMessageId` to ensure proper routing
- **Error handling**: Graceful error handling with client notification
- **Health checks**: Built-in health check endpoint
- **CORS support**: Configurable CORS for cross-origin requests

## Installation

```bash
# Navigate to the SSE service directory
cd src/sse_service

# Install dependencies using uv
uv sync
```

## Configuration

Copy `.env.example` to `.env` and configure the following variables:

- `SERVICEBUS_FULLY_QUALIFIED_NAMESPACE`: Your Azure Service Bus namespace
- `SERVICEBUS_TOKEN_STREAMS_TOPIC`: The topic name for token streams
- `SERVICEBUS_TOKEN_STREAMS_SUBSCRIPTION`: The subscription name for this service
- `CORS_ORIGINS`: Allowed CORS origins (comma-separated)
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)

## Running

```bash
# Using uv
uv run python main.py

# Or with uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

## API Endpoints

### GET /api/stream/{sessionId}/{chatMessageId}

Establishes an SSE connection to stream tokens for a specific chat message.

**Parameters:**
- `sessionId`: The session identifier
- `chatMessageId`: The specific chat message identifier

**Response:** Server-Sent Events stream with the following data formats:
- Token: `data: {"token": "text"}`
- End of stream: `data: __END__`
- Error: `data: {"error": "message"}`

### GET /health

Health check endpoint that returns service status.

**Response:**
```json
{
  "status": "healthy",
  "service": "sse-service"
}
```

## Architecture

The SSE service operates independently from the front service, allowing for better scalability:

1. **Receives requests**: Clients connect to `/api/stream/{sessionId}/{chatMessageId}`
2. **Opens session receiver**: Creates a session-aware Service Bus receiver for the given session
3. **Filters messages**: Only processes tokens matching the requested `chatMessageId`
4. **Streams tokens**: Sends tokens to the client via Server-Sent Events
5. **Handles completion**: Sends end-of-stream signal when the response is complete

## Scaling

The SSE service can be scaled independently based on streaming demand:

- Scale horizontally by running multiple instances
- Each instance handles its own set of SSE connections
- No shared state between instances (stateless design)
- Load balancing across instances for optimal resource utilization

## Error Handling

- Connection errors are handled gracefully
- Malformed messages are logged and skipped
- Client disconnections are detected and resources cleaned up
- Service Bus errors result in appropriate error messages to clients
