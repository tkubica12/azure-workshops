# Scalable Chat Worker Service

This worker service listens to the `user-messages` Azure Service Bus topic (via a specific subscription). When it receives a message, it processes the content and streams response tokens back to the `token-streams` Service Bus topic. The front-end service consumes these tokens and forwards them to the appropriate client via Server-Sent Events (SSE).

## Message Handling

1.  **Receiving Messages**:
    *   The worker picks up messages from its subscription on the `user-messages` topic.
    *   The message body is expected to be a JSON string containing:
        *   `text`: The user's query.
        *   `sessionId`: A unique identifier for the user's session.
        *   `messageId`: A unique identifier for the specific message within that session.

2.  **Processing Messages**:
    *   The worker (currently) simulates LLM processing by generating a static response based on the input text and `messageId`.
    *   It streams this response character by character (as tokens).

3.  **Sending Response Tokens**:
    *   For each character (token) in the response, the worker sends a new message to the `token-streams` topic.
    *   Each token message body is a JSON string containing:
        *   `sessionId`: The original session ID from the input message.
        *   `messageId`: The original message ID from the input message.
        *   `token`: The character (token) being sent.
    *   After all tokens for a response have been sent, the worker sends a final end-of-stream (EOS) sentinel message to the `token-streams` topic.
    *   The EOS message body is a JSON string containing:
        *   `sessionId`: The original session ID.
        *   `messageId`: The original message ID.
        *   `end_of_stream`: `true`.

This `sessionId` and `messageId` are crucial for the front service to correctly route tokens and the EOS signal to the specific client and message stream that initiated the request.

## Setup

1.  Copy `.env.example` to `.env` and configure the following variables:

    ```dotenv
    SERVICEBUS_FULLY_QUALIFIED_NAMESPACE=<your-service-bus-namespace>.servicebus.windows.net
    SERVICEBUS_USER_MESSAGES_TOPIC=user-messages
    SERVICEBUS_USER_MESSAGES_SUBSCRIPTION=worker-service # Or your specific subscription name
    SERVICEBUS_TOKEN_STREAMS_TOPIC=token-streams
    LOG_LEVEL=INFO # Recommended: INFO or DEBUG for development
    ```

2.  Install dependencies (e.g., using `uv` or `pip` based on your project setup):

    ```bash
    # If using uv and requirements.txt is present
    uv pip install -r requirements.txt 
    # Or if you have a pyproject.toml with dependencies
    # uv install
    ```

3.  Run the worker:

    ```bash
    # If using uv
    uv run python main.py 
    # Or directly with python
    # python main.py
    ```

## Demo Behavior

Currently, the worker sends a static response string, character by character, with a short delay (e.g., 0.1 seconds) between each character. It includes the original `messageId` in its response. It then sends an `end_of_stream` sentinel message (also containing the `sessionId` and `messageId`) to signal the end of the stream for that specific message.

## Graceful Shutdown and Container Lifecycle

**LLM Worker Graceful Shutdown:** The LLM worker service implements graceful shutdown to handle scale-down events properly. When a `SIGTERM` signal is received (typical in container orchestration environments like Azure Container Apps), the worker:

1. **Stops accepting new messages** from the Service Bus queue
2. **Continues processing existing LLM calls** that are already in progress  
3. **Waits for all active tasks to complete** before shutting down
4. **Uses a 4-minute timeout** to allow sufficient time for LLM responses to complete

This ensures that user requests are not lost during scale-down events and that partial responses are properly completed and streamed to clients.

**Container Apps Configuration:** The Azure Container Apps deployment is configured with a `terminationGracePeriodSeconds` of 240 seconds (4 minutes) to align with the worker's shutdown timeout. This extended grace period (increased from the default 30 seconds) provides adequate time for:
- Long-running LLM API calls to complete
- Token streaming to finish properly  
- Proper message settlement in Service Bus
- Clean resource cleanup

**Implementation Details:** The graceful shutdown mechanism:
- Uses Python's `signal` module to handle `SIGTERM` and `SIGINT` signals
- Employs an `asyncio.Event` to coordinate shutdown across all async tasks
- Tracks active message processing tasks and waits for their completion
- Abandons unprocessed messages so they can be picked up by other worker instances
- Provides detailed logging for monitoring shutdown progress

This approach ensures high reliability during scaling events and prevents message loss or incomplete responses that could degrade user experience.
