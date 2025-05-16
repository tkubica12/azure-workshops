# Scalable Chat Front Service

This service implements the **Front Service** component of the scalable chat architecture.

Key responsibilities:
- Exposes an HTTP endpoint (`POST /api/session/start`) to initiate a chat session and provide a `sessionId`.
- Exposes an HTTP endpoint (`POST /api/chat`) to receive user questions, `sessionId`, and a client-generated `messageId`.
- Initiates a Server-Sent Events (SSE) stream back to the client for the duration of the chat request.
- Enqueues incoming questions (including `text`, `sessionId`, and `messageId`) onto an Azure Service Bus Topic (`user-messages`).
- Listens for response tokens from another Azure Service Bus Topic (`token-streams`), specifically for its subscription.
- Forwards these tokens to the correct client via the SSE stream, based on `sessionId`.
- Sends an `__END__` signal over SSE when the worker indicates the end of a stream for a particular `messageId`.

Configuration:
- Uses `DefaultAzureCredentials` from `azure-identity` for authentication in Azure.
- Local development: configuration loaded from `.env` via `python-dotenv`.
- Environment variables:
  - `SERVICEBUS_FULLY_QUALIFIED_NAMESPACE` (e.g., `mysb.servicebus.windows.net`)
  - `SERVICEBUS_USER_MESSAGES_TOPIC` (topic to send user questions to workers)
  - `SERVICEBUS_TOKEN_STREAMS_TOPIC` (topic to receive token streams from workers)
  - `SERVICEBUS_TOKEN_STREAMS_SUBSCRIPTION` (subscription for this front service instance to receive token streams)
  - `LOG_LEVEL` (e.g., `INFO`, `DEBUG`, `WARNING`)
  - `OS_ENV` (`local` vs `prod`) - *Note: This variable was mentioned but isn't explicitly used in the provided `main.py` snippet. If used, its purpose should be clarified here.*
  - Optional: other Azure resources connection strings or identifiers.

Endpoints:
- `POST /api/session/start`:
  - Request: (No body needed)
  - Response: `{"sessionId": "<generated-uuid>"}`
- `POST /api/chat`:
  - Request Body: `{"message": "user question", "sessionId": "<session-id>", "messageId": "<client-generated-uuid>"}`
  - Response: SSE stream (`text/event-stream`)
    - Data events: `data: {"token": "<char_token>"}\n\n`
    - End-of-message signal: `data: __END__\n\n`

The OpenAPI spec is available at `/openapi.json` and UI docs at `/docs` when running the FastAPI application.

Architecture:
```mermaid
flowchart LR
  Client -->|POST /api/session/start| Front(Front Service)
  Front -->|sessionId| Client

  Client -->|POST /api/chat (message, sessionId, messageId)| Front
  Front -->|enqueue (text, sessionId, messageId)| SBUserMessages(Service Bus: user-messages Topic)
  Front -->|SSE Stream| Client

  WorkerService -->|publish (token/EOS, sessionId, messageId)| SBTokenStreams(Service Bus: token-streams Topic)
  SBTokenStreams -->|receive| Front
  Front -->|SSE data (token) or __END__| Client
```

## Message Flow for /api/chat:

1.  **Client to Front Service**: Client sends `POST /api/chat` with `message`, `sessionId`, and `messageId`.
2.  **Front Service**: 
    a.  Validates input.
    b.  Creates an `asyncio.Queue` for the `sessionId` if one doesn't exist (used to buffer tokens for the SSE stream).
    c.  Constructs a `ServiceBusMessage` containing the `text`, `sessionId`, and `messageId`. The `sessionId` is also set as the `session_id` property of the Service Bus message for potential session-aware processing if the `user-messages` topic/subscription is configured for sessions.
    d.  Sends this message to the `SERVICEBUS_USER_MESSAGES_TOPIC`.
    e.  Returns an SSE `StreamingResponse` to the client, which will pull tokens from the session-specific `asyncio.Queue`.
3.  **Front Service (Background Listener)**:
    a.  Continuously listens to its subscription on `SERVICEBUS_TOKEN_STREAMS_TOPIC`.
    b.  When a message arrives (containing `token` or `end_of_stream`, along with `sessionId` and `messageId` from the worker):
        i.  It looks up the `asyncio.Queue` for the `sessionId`.
        ii. Puts the `{"token": "...", "messageId": "..."}` or `{"end_of_stream": True, "messageId": "..."}` dictionary into that queue.
4.  **Front Service (SSE Generator for Client)**:
    a.  The `token_stream_generator` for the specific `/api/chat` request awaits items from its `sessionId`'s `asyncio.Queue`.
    b.  When a `{"token": "..."}` item appears, it sends `data: {"token": "..."}\n\n` to the client.
    c.  When an `{"end_of_stream": True, "messageId": "..."}` item appears that matches the `initial_messageId` of the stream, it sends `data: __END__\n\n` to the client and closes that specific message stream.
