# Scalable Chat History Worker Service

This worker service listens to the `message-completed` Azure Service Bus topic and persists conversation history to Azure Cosmos DB for long-term storage. It provides asynchronous history persistence with conversation title generation.

## Message Handling

1. **Receiving Message-Completed Events**:
   - The worker picks up messages from its subscription on the `message-completed` topic.
   - The message body is expected to be a JSON string containing:
     - `sessionId`: The unique identifier for the conversation session.
     - `userId`: The user who participated in the conversation.
     - `chatMessageId`: The unique identifier for the specific message within that session.
     - `completedAt`: Timestamp when the message was completed.
     - `eventType`: Should be "message_completed".

2. **Processing Messages**:
   - The worker fetches the complete conversation data from Redis using the `sessionId`.
   - If the conversation doesn't have a title, it generates one using the LLM API based on the full conversation history (up to 6 messages for context).
   - The conversation is then persisted to Azure Cosmos DB for long-term storage.

3. **Cosmos DB Storage**:
   - Each conversation is stored as a document with:
     - `id`: The sessionId (used as document ID)
     - `userId`: Used as the partition key for efficient querying
     - `title`: Generated conversation title
     - `messages`: Array of all conversation messages
     - `createdAt`, `lastActivity`, `persistedAt`: Timestamps

## Architecture Components

- **Azure Service Bus**: Message-completed topic subscription for event-driven processing
- **Azure Managed Redis**: Source of conversation data (24-hour TTL hot cache)
- **Azure Cosmos DB**: Long-term persistent storage for conversation history
- **Azure AI Inference**: LLM API for generating conversation titles
- **Azure Monitor**: Observability and logging

## Setup

### Prerequisites

- Python 3.12+
- uv package manager
- Azure Service Bus namespace
- Azure Cosmos DB account
- Azure Managed Redis cache
- Azure AI Inference endpoint

### Environment Variables

Create a `.env` file with the following variables:

```env
SERVICEBUS_FULLY_QUALIFIED_NAMESPACE=your-servicebus.servicebus.windows.net
SERVICEBUS_MESSAGE_COMPLETED_TOPIC=message-completed
SERVICEBUS_MESSAGE_COMPLETED_SUBSCRIPTION=history-worker-message-completed
COSMOS_ENDPOINT=https://your-cosmos.documents.azure.com:443/
COSMOS_DATABASE_NAME=mydb
COSMOS_CONTAINER_NAME=mydocuments
AZURE_AI_CHAT_ENDPOINT=https://your-ai-service.openai.azure.com/openai/deployments/gpt-4
REDIS_HOST=your-redis.redis.azure.net
REDIS_PORT=10000
REDIS_SSL=true
LOG_LEVEL=INFO
MAX_CONCURRENCY=10
APPLICATIONINSIGHTS_CONNECTION_STRING=your-app-insights-connection-string
OTEL_SERVICE_NAME=history-worker
```

### Installation

```bash
# Install dependencies using uv
uv sync

# Run the service
uv run python main.py
```

### Docker

```bash
# Build the Docker image
docker build -t history-worker .

# Run the container
docker run --env-file .env history-worker
```

## Authentication

The service uses **Azure Managed Identity** for authentication to:

- **Azure Service Bus**: Uses DefaultAzureCredential for Service Bus operations
- **Azure Cosmos DB**: Uses DefaultAzureCredential for Cosmos DB operations  
- **Azure Managed Redis**: Uses Entra ID authentication via redis-entraid
- **Azure AI Inference**: Uses DefaultAzureCredential for LLM API calls

Ensure the service's managed identity has appropriate RBAC permissions:

- `Azure Service Bus Data Receiver` role on the Service Bus namespace
- Custom Cosmos DB role with read/write permissions on the database/container
- `Redis Data Contributor` role on the Redis cache
- `Cognitive Services User` role on the AI service

## Conversation Title Generation

The service automatically generates conversation titles when they don't exist:

1. Extracts the first user message from the conversation
2. Uses the LLM API to generate a concise, descriptive title (3-6 words)
3. Cleans and validates the generated title
4. Falls back to "New Conversation" if generation fails

## Data Schema

### Cosmos DB Document Structure

```json
{
  "id": "sess_abc123",
  "sessionId": "sess_abc123", 
  "userId": "user_001",
  "title": "Machine Learning Discussion",
  "createdAt": "2025-06-05T10:00:00Z",
  "lastActivity": "2025-06-05T11:30:00Z",
  "persistedAt": "2025-06-05T11:35:00Z",
  "messages": [
    {
      "messageId": "msg_001",
      "role": "user",
      "content": "What is machine learning?",
      "timestamp": "2025-06-05T10:00:00Z"
    },
    {
      "messageId": "msg_002",
      "role": "assistant", 
      "content": "Machine learning is a subset of artificial intelligence...",
      "timestamp": "2025-06-05T10:00:15Z"
    }
  ]
}
```

## Graceful Shutdown and Container Lifecycle

The service implements proper graceful shutdown handling:

- **Signal Handling**: Responds to `SIGTERM` and `SIGINT` signals
- **Message Settlement**: Completes or abandons in-flight messages appropriately
- **Resource Cleanup**: Closes database and cache connections properly
- **Timeout Handling**: 60-second timeout for completing active tasks

This ensures reliable operation during container restarts and scaling events without data loss.

## Error Handling

- **Message Processing Errors**: Failed messages are dead-lettered for investigation
- **Redis Connection Issues**: Logged as warnings, processing continues for other messages
- **Cosmos DB Errors**: Detailed logging with retry capabilities
- **Title Generation Failures**: Falls back to default title, doesn't block persistence

## Monitoring and Observability

The service integrates with Azure Monitor and OpenTelemetry for comprehensive observability:

- **Distributed Tracing**: End-to-end request tracing across services
- **Metrics**: Processing rates, error rates, and performance metrics
- **Logging**: Structured logging with correlation IDs
- **Health Checks**: Built-in health monitoring for dependencies

## Scaling

The service supports horizontal scaling through:

- **Stateless Design**: No local state dependencies
- **Competing Consumers**: Multiple instances can process messages concurrently
- **Backpressure Handling**: Configurable concurrency limits prevent overload
- **Session-Aware Processing**: Service Bus sessions ensure message ordering when needed
