import os
import json
import logging
from datetime import datetime
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from azure.identity import DefaultAzureCredential
from azure.cosmos import CosmosClient, PartitionKey, exceptions
import uvicorn
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace

# Load local .env when in development
load_dotenv()

# Read configuration from environment
COSMOS_ENDPOINT = os.getenv("COSMOS_ENDPOINT")
COSMOS_DATABASE_NAME = os.getenv("COSMOS_DATABASE_NAME", "chat")
COSMOS_CONTAINER_NAME = os.getenv("COSMOS_CONTAINER_NAME", "conversations")

if not COSMOS_ENDPOINT:
    raise RuntimeError("Missing Cosmos DB configuration in environment variables")

# Logging configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'WARNING').upper()
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)

# Azure Monitor configuration
configure_azure_monitor(
    enable_live_metrics=True,
    instrumentation_options={
        "azure_sdk": {"enabled": True},
        "django": {"enabled": False},
        "fastapi": {"enabled": True},
        "flask": {"enabled": False},
        "psycopg2": {"enabled": False},
        "requests": {"enabled": False},
        "urllib": {"enabled": False},
        "urllib3": {"enabled": False},
    }
)
tracer = trace.get_tracer(__name__)

# Initialize Azure credentials and clients
credential = DefaultAzureCredential()
cosmos_client = CosmosClient(COSMOS_ENDPOINT, credential)
database = cosmos_client.get_database_client(COSMOS_DATABASE_NAME)
container = database.get_container_client(COSMOS_CONTAINER_NAME)

# FastAPI app
app = FastAPI(
    title="Scalable Chat History API",
    version="0.1.0",
    description="API for retrieving conversation history from Cosmos DB",
)

# Configure CORS
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")
allowed_origins = [origin.strip() for origin in CORS_ORIGINS.split(",") if origin.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# Pydantic models
class Message(BaseModel):
    messageId: str
    role: str 
    content: str
    timestamp: str  # ISO format string

class Conversation(BaseModel):
    sessionId: str
    userId: str
    title: Optional[str] = None
    lastActivity: str  # ISO format string
    messageCount: int

class ConversationDetail(BaseModel):
    sessionId: str
    userId: str
    title: Optional[str] = None
    messages: List[Message]

class UpdateTitleRequest(BaseModel):
    title: str

# Helper functions
def get_conversation_from_cosmos(session_id: str) -> Optional[Dict]:
    """Retrieve conversation from Cosmos DB"""
    try:
        item = container.read_item(item=session_id, partition_key=session_id)
        return item
    except exceptions.CosmosResourceNotFoundError:
        return None
    except Exception as e:
        logger.error(f"Failed to retrieve conversation {session_id} from Cosmos DB: {e}")
        return None

def get_user_conversations_from_cosmos(user_id: str, limit: int = 50) -> List[Dict]:
    """Get user's conversations from Cosmos DB"""
    try:
        query = """
        SELECT c.sessionId, c.userId, c.title, c.lastActivity, ARRAY_LENGTH(c.messages) as messageCount
        FROM c 
        WHERE c.userId = @userId 
        ORDER BY c.lastActivity DESC
        OFFSET 0 LIMIT @limit
        """
        items = list(container.query_items(
            query=query,
            parameters=[
                {"name": "@userId", "value": user_id},
                {"name": "@limit", "value": limit}
            ],
            enable_cross_partition_query=True
        ))
        return items
    except Exception as e:
        logger.error(f"Failed to get conversations for user {user_id} from Cosmos DB: {e}")
        return []

def update_conversation_title_in_cosmos(session_id: str, title: str) -> bool:
    """Update conversation title in Cosmos DB"""
    try:
        # Read existing item
        item = container.read_item(item=session_id, partition_key=session_id)
        item['title'] = title
        container.replace_item(item=session_id, body=item)
        return True
    except exceptions.CosmosResourceNotFoundError:
        return False
    except Exception as e:
        logger.error(f"Failed to update title for conversation {session_id}: {e}")
        return False

# API endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "history-api"}

@app.get("/conversations/{user_id}", response_model=List[Conversation])
async def get_user_conversations(user_id: str, limit: int = 50):
    """Get list of conversations for a user"""
    logger.info(f"Getting conversations for user: {user_id}")
    
    conversations = get_user_conversations_from_cosmos(user_id, limit)
    
    result = []
    for conv in conversations:
        result.append(Conversation(
            sessionId=conv.get('sessionId'),
            userId=conv.get('userId'),
            title=conv.get('title'),
            lastActivity=conv.get('lastActivity', ''),
            messageCount=conv.get('messageCount', 0)
        ))
    
    logger.info(f"Found {len(result)} conversations for user {user_id}")
    return result

@app.get("/conversations/{user_id}/{session_id}/messages", response_model=ConversationDetail)
async def get_conversation_messages(user_id: str, session_id: str):
    """Get all messages for a specific conversation"""
    logger.info(f"Getting messages for conversation {session_id} (user: {user_id})")
    
    # Get conversation data from Cosmos DB
    conversation_data = get_conversation_from_cosmos(session_id)
    
    if not conversation_data:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Verify user owns this conversation
    if conversation_data.get('userId') != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    messages = []
    for msg in conversation_data.get('messages', []):
        messages.append(Message(
            messageId=msg.get('messageId'),
            role=msg.get('role'),
            content=msg.get('content'),
            timestamp=msg.get('timestamp', '')
        ))
    
    logger.info(f"Found {len(messages)} messages for conversation {session_id}")
    
    return ConversationDetail(
        sessionId=session_id,
        userId=user_id,
        title=conversation_data.get('title'),
        messages=messages
    )

@app.put("/conversations/{user_id}/{session_id}/title")
async def update_conversation_title(user_id: str, session_id: str, request: UpdateTitleRequest):
    """Update conversation title"""
    logger.info(f"Updating title for conversation {session_id} (user: {user_id}) to '{request.title}'")
    
    # Verify conversation exists and user owns it
    conversation_data = get_conversation_from_cosmos(session_id)
    
    if not conversation_data:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    if conversation_data.get('userId') != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Update title in Cosmos DB
    success = update_conversation_title_in_cosmos(session_id, request.title)
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to update conversation title")
    
    logger.info(f"Successfully updated title for conversation {session_id}")
    return {"success": True, "message": "Title updated successfully"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8005, reload=True)
