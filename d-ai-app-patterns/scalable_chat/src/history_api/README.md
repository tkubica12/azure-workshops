# Scalable Chat History API

This service implements the **History API** component of the scalable chat architecture.

## Key Responsibilities

- **Conversation History**: Retrieves conversation list for users from Cosmos DB
- **Message Retrieval**: Gets detailed message history for specific conversations from Cosmos DB
- **Title Management**: Allows users to update conversation titles
- **Data Source**: Reads from Cosmos DB (long-term storage)

## Configuration

Environment variables:
- `COSMOS_ENDPOINT` - Azure Cosmos DB endpoint
- `COSMOS_DATABASE_NAME` - Cosmos DB database name (default: "chat")
- `COSMOS_CONTAINER_NAME` - Cosmos DB container name (default: "conversations")
- `LOG_LEVEL` - Logging level (default: WARNING)
- `CORS_ORIGINS` - Allowed CORS origins (default: *)
- `APPLICATIONINSIGHTS_CONNECTION_STRING` - Application Insights connection string

## API Endpoints

### GET /conversations/{user_id}
Get list of conversations for a user with metadata.

**Response:**
```json
[
  {
    "sessionId": "uuid",
    "userId": "user_001",
    "title": "Conversation about AI",
    "lastActivity": "2025-01-01T12:00:00Z",
    "messageCount": 15
  }
]
```

### GET /conversations/{user_id}/{session_id}/messages
Get all messages for a specific conversation.

**Response:**
```json
{
  "sessionId": "uuid",
  "userId": "user_001", 
  "title": "Conversation about AI",
  "messages": [
    {
      "id": "msg_uuid",
      "sender": "user",
      "content": "Hello!",
      "timestamp": "2025-01-01T12:00:00Z"
    }
  ]
}
```

### PUT /conversations/{user_id}/{session_id}/title
Update conversation title.

**Request:**
```json
{
  "title": "New conversation title"
}
```

## Architecture

The service reads conversation history from Cosmos DB where conversations are persisted by the history worker service.

Data flow:
1. History worker persists conversations to Cosmos DB after completion
2. History API serves conversation lists and detailed messages from Cosmos DB
3. Title updates are persisted directly to Cosmos DB
