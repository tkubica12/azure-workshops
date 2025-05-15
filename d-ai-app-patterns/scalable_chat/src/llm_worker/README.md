# Scalable Chat Worker Service

This worker service receives user messages from the `user-messages` Service Bus topic, processes them, and streams response tokens to the `token-streams` topic for the front-end to consume via SSE.

## Setup

1. Copy `.env.example` to `.env` and configure the following variables:

```
SERVICEBUS_FULLY_QUALIFIED_NAMESPACE=<your-service-bus-namespace>.servicebus.windows.net
SERVICEBUS_USER_MESSAGES_TOPIC=user-messages
SERVICEBUS_USER_MESSAGES_SUBSCRIPTION=worker-service
SERVICEBUS_TOKEN_STREAMS_TOPIC=token-streams
LOG_LEVEL=INFO
```

2. Install dependencies using `uv`:

```bash
uv install
```

3. Run the worker:

```bash
uv run main:main
```

## Demo Behavior

Currently, the worker sends a static response string, character by character, with a 1 second delay between each character. It then sends an `__END__` sentinel to signal end of stream.
