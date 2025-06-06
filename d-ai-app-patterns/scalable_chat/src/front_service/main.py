import os
import json
import logging
import asyncio
import uuid
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from azure.identity.aio import DefaultAzureCredential
from azure.servicebus.aio import ServiceBusClient, ServiceBusSender
from azure.servicebus import ServiceBusMessage
from contextlib import asynccontextmanager
import uvicorn
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace

# Load local .env when in development
load_dotenv()

# Read configuration from environment
SERVICEBUS_FULLY_QUALIFIED_NAMESPACE = os.getenv("SERVICEBUS_FULLY_QUALIFIED_NAMESPACE")
SERVICEBUS_USER_MESSAGES_TOPIC = os.getenv("SERVICEBUS_USER_MESSAGES_TOPIC")

if not SERVICEBUS_FULLY_QUALIFIED_NAMESPACE or not SERVICEBUS_USER_MESSAGES_TOPIC:
    raise RuntimeError("Missing Service Bus configuration in environment variables")

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

# Initialize Azure credentials
credential = DefaultAzureCredential()

# Global ServiceBusClient
sb_client: ServiceBusClient | None = None
SERVICEBUS_SENDER_POOL_SIZE = int(os.getenv("SERVICEBUS_SENDER_POOL_SIZE", "10"))
sender_pool: asyncio.Queue | None = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global sb_client, sender_pool

    local_sb_client = None
    
    try:
        logger.info("Application startup: Initializing Service Bus client.")
        local_sb_client = ServiceBusClient(
            fully_qualified_namespace=SERVICEBUS_FULLY_QUALIFIED_NAMESPACE,
            credential=credential
        )
        # Assign to global client
        sb_client = local_sb_client
        # Initialize sender pool
        logger.info(f"Application startup: Creating {SERVICEBUS_SENDER_POOL_SIZE}-size Service Bus sender pool.")
        local_pool: asyncio.Queue = asyncio.Queue()
        for _ in range(SERVICEBUS_SENDER_POOL_SIZE):
            sender = local_sb_client.get_topic_sender(SERVICEBUS_USER_MESSAGES_TOPIC)
            # Open AMQP link once per sender
            await sender.__aenter__()
            lock = asyncio.Lock()
            await local_pool.put((sender, lock))
        sender_pool = local_pool
        
        yield  # Application runs

    finally:
        # Close all pooled senders
        if sender_pool:
            logger.info("Application shutdown: Closing Service Bus sender pool.")
            while not sender_pool.empty():
                sender, _ = await sender_pool.get()
                # Cleanly close AMQP link for each sender
                await sender.__aexit__(None, None, None)
        # Close client
        logger.info("Application shutdown: Closing Service Bus client.")
        if local_sb_client:
            await local_sb_client.close()
        # Close credentials
        await credential.close()
        # Reset globals
        sb_client = None
        sender_pool = None

app = FastAPI(
    title="Scalable Chat Front Service",
    version="0.1.0",
    description="Front-end for scalable chat using SSE and Azure Service Bus",
    lifespan=lifespan,
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

class SessionStartRequest(BaseModel):
    userId: str

class ChatMessage(BaseModel):
    message: str
    sessionId: str
    chatMessageId: str
    userId: str

class ChatResponse(BaseModel):
    success: bool
    chatMessageId: str
    sessionId: str
    message: str = "Message queued for processing"

class SessionStartResponse(BaseModel):
    sessionId: str

@app.post("/api/session/start", response_model=SessionStartResponse)
async def start_session(session_request: SessionStartRequest):
    sessionId = str(uuid.uuid4())
    logger.info(f"New session started: {sessionId} for user: {session_request.userId}")
    return SessionStartResponse(sessionId=sessionId)

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(chat_message: ChatMessage, request: Request):
    global sb_client, sender_pool
    if not sb_client:
        raise HTTPException(status_code=503, detail="Service Bus client not initialized.")
    if not sender_pool:
        raise HTTPException(status_code=503, detail="Service Bus sender pool not initialized.")    
    logger.info(f"Received message: '{chat_message.message}' for session: {chat_message.sessionId}, chatMessageId: {chat_message.chatMessageId}, userId: {chat_message.userId}")

    try:
        message_to_send = ServiceBusMessage(
            body=json.dumps({
                "text": chat_message.message,
                "sessionId": chat_message.sessionId,
                "chatMessageId": chat_message.chatMessageId,
                "userId": chat_message.userId
            }),
            message_id=chat_message.chatMessageId,
            session_id=chat_message.sessionId
        )
        # Acquire a sender and its lock from the pool
        sender, lock = await sender_pool.get()
        try:
            async with lock:
                await sender.send_messages(message_to_send)
        finally:
            # Return sender to pool
            await sender_pool.put((sender, lock))
        logger.info(f"Message {chat_message.chatMessageId} for session {chat_message.sessionId} sent to topic '{SERVICEBUS_USER_MESSAGES_TOPIC}'")
        
        return ChatResponse(
            success=True,
            chatMessageId=chat_message.chatMessageId,
            sessionId=chat_message.sessionId
        )
        
    except Exception as e:
        logger.error(f"Failed to send message to Service Bus for session {chat_message.sessionId}, chatMessageId {chat_message.chatMessageId}: {e}")
        raise HTTPException(status_code=500, detail="Failed to process message.")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)