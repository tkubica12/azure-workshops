# Scalable Chat Memory API

This service implements the **Memory API/MCP** component of the scalable chat architecture.

## Key Responsibilities

- **User Memory Management**: Stores and retrieves structured user profiles and preferences from Cosmos DB
- **Conversation Memory**: Manages conversation summaries with vector embeddings for semantic search
- **Dual Interface**: Provides both REST API (for Client UI) and internal endpoints (for Memory Worker)
- **Memory Retrieval**: Enables Worker Service to fetch relevant user memories during LLM processing
- **Data Source**: Reads from and writes to Cosmos DB (long-term memory storage)

## Configuration

Environment variables:
- `COSMOS_ENDPOINT` - Azure Cosmos DB endpoint
- `COSMOS_DATABASE_NAME` - Cosmos DB database name (default: "memory")
- `COSMOS_CONVERSATIONS_CONTAINER_NAME` - Conversations container name (default: "conversations")
- `COSMOS_USER_MEMORIES_CONTAINER_NAME` - User memories container name (default: "user-memories")
- `LOG_LEVEL` - Logging level (default: WARNING)
- `CORS_ORIGINS` - Allowed CORS origins (default: *)
- `PORT` - Service port (default: 8003)
- `APPLICATIONINSIGHTS_CONNECTION_STRING` - Application Insights connection string

## API Endpoints

### GET /api/memory/users/{user_id}/memories
Get structured memories for a specific user.

**Response:**
```json
{
  "userId": "user_001",
  "output_preferences": {
    "length": "detailed",
    "format": "markdown"
  },
  "personal_preferences": {
    "name": "John",
    "pronouns": "he/him"
  },
  "assistant_preferences": {
    "name": "Assistant",
    "style": "professional"
  },
  "knowledge": ["machine learning", "python"],
  "interests": ["AI", "technology"],
  "dislikes": ["interruptions"],
  "family_and_friends": {
    "spouse": "Jane",
    "children": 2
  },
  "work_profile": {
    "role": "Data Scientist",
    "company": "Tech Corp"
  },
  "goals": ["Learn deep learning", "Get promoted"],
  "last_updated": "2025-01-01T12:00:00Z"
}
```

### POST /api/memory/users/{user_id}/memories/search
Search conversational memories for a specific user.

**Request:**
```json
{
  "query": "machine learning discussions",
  "limit": 10
}
```

**Response:**
```json
[
  {
    "sessionId": "sess_abc123",
    "summary": "User discussed machine learning concepts and asked about neural networks",
    "timestamp": "2025-01-01T12:00:00Z",
    "themes": ["machine learning", "neural networks"],
    "persons": ["John"],
    "places": ["office"],
    "user_sentiment": "positive",
    "relevance_score": 0.95
  }
]
```

## Internal Endpoints (for Memory Worker)

### POST /internal/conversation-memory
Store or update a conversation memory.

**Request:**
```json
{
  "sessionId": "sess_abc123",
  "userId": "user_001",
  "summary": "Discussion about AI and machine learning",
  "themes": ["AI", "machine learning"],
  "persons": ["John"],
  "places": ["office"],
  "user_sentiment": "positive",
  "vector_embedding": [0.1, 0.2, 0.3, ...]
}
```

### POST /internal/user-memory
Update user memory profile.

**Request:**
```json
{
  "userId": "user_001",
  "updates": {
    "interests": ["deep learning"],
    "knowledge": ["neural networks"],
    "goals": ["Master PyTorch"]
  }
}
```

## Architecture

The service manages two main data collections in Cosmos DB:

### Conversations Collection
Stores conversation summaries with vector embeddings for semantic search:
- `sessionId`: Unique conversation identifier
- `userId`: User who participated in the conversation
- `summary`: LLM-generated conversation summary
- `timestamp`: When the summary was created
- `themes`: Key topics discussed
- `persons`: Named individuals mentioned
- `places`: Locations mentioned
- `user_sentiment`: User's sentiment during conversation
- `vector_embedding`: Embedding vector for semantic search

### User-Memories Collection
Stores structured user profiles and preferences:
- `userId`: Unique user identifier (partition key)
- `output_preferences`: User's preferred output styles
- `personal_preferences`: How user prefers to be addressed
- `assistant_preferences`: User's preferences for assistant behavior
- `knowledge`: Topics where user has demonstrated understanding
- `interests`: User's hobbies and interests
- `dislikes`: Topics or styles user dislikes
- `family_and_friends`: Personal connections user has shared
- `work_profile`: Professional information
- `goals`: User's stated objectives
- `last_updated`: When the profile was last modified

## Data Flow

1. **Memory Worker** processes completed conversations and calls internal endpoints
2. **Memory API** stores conversation summaries and updates user profiles in Cosmos DB
3. **Client UI** requests user memories via REST API for display
4. **Worker Service** (via MCP interface) fetches relevant memories during LLM processing

## Setup

### Prerequisites

- Python 3.12+
- uv package manager
- Azure Cosmos DB account
- Azure Monitor (optional)

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
docker build -t memory-api .

# Run the container
docker run -p 8003:8003 \
  -e COSMOS_ENDPOINT=https://your-cosmos.documents.azure.com:443/ \
  -e COSMOS_DATABASE_NAME=memory \
  memory-api
```
