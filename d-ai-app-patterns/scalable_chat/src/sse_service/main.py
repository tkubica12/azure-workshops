import os
import json
import logging
import asyncio
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from azure.identity.aio import DefaultAzureCredential
from azure.servicebus.aio import ServiceBusClient
from contextlib import asynccontextmanager
import uvicorn
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace

# Load local .env when in development
load_dotenv()

# Read configuration from environment
SERVICEBUS_FULLY_QUALIFIED_NAMESPACE = os.getenv("SERVICEBUS_FULLY_QUALIFIED_NAMESPACE")
SERVICEBUS_TOKEN_STREAMS_TOPIC = os.getenv("SERVICEBUS_TOKEN_STREAMS_TOPIC")
SERVICEBUS_TOKEN_STREAMS_SUBSCRIPTION = os.getenv("SERVICEBUS_TOKEN_STREAMS_SUBSCRIPTION")

if not SERVICEBUS_FULLY_QUALIFIED_NAMESPACE or not SERVICEBUS_TOKEN_STREAMS_TOPIC or not SERVICEBUS_TOKEN_STREAMS_SUBSCRIPTION:
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

@asynccontextmanager
async def lifespan(app: FastAPI):
    global sb_client
    
    local_sb_client = None
    
    try:
        logger.info("SSE Service startup: Initializing Service Bus client.")
        local_sb_client = ServiceBusClient(
            fully_qualified_namespace=SERVICEBUS_FULLY_QUALIFIED_NAMESPACE,
            credential=credential
        )
        # Assign to global client
        sb_client = local_sb_client
        
        yield  # Application runs

    finally:
        # Close client
        logger.info("SSE Service shutdown: Closing Service Bus client.")
        if local_sb_client:
            await local_sb_client.close()
        # Close credentials
        await credential.close()
        # Reset globals
        sb_client = None

app = FastAPI(
    title="Scalable Chat SSE Service",
    version="0.1.0",
    description="Server-Sent Events streaming service for scalable chat",
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

async def token_stream_generator(sessionId: str, chatMessageId: str):
    """
    Generator that streams tokens for a specific chat message from Service Bus.
    Uses session-aware receiver to get tokens for the specified session.
    """
    logger.info(f"Opening sessionful receiver for token streams for session: {sessionId}, message: {chatMessageId}")
    
    try:
        async with sb_client.get_subscription_receiver(
            SERVICEBUS_TOKEN_STREAMS_TOPIC,
            SERVICEBUS_TOKEN_STREAMS_SUBSCRIPTION,
            session_id=sessionId
        ) as receiver:
            logger.info(f"Token stream receiver opened for session: {sessionId}")
            
            async for sb_msg in receiver:
                logger.debug("Received chunk: %s", sb_msg)
                try:
                    data = json.loads(str(sb_msg))
                    
                    # Only process tokens for the matching chatMessageId
                    if data.get("chatMessageId") != chatMessageId:
                        await receiver.complete_message(sb_msg)
                        continue
                    
                    # End-of-stream signal
                    if data.get("end_of_stream"):
                        yield "data: __END__\n\n"
                        await receiver.complete_message(sb_msg)
                        break
                    
                    # Token data event
                    token = data.get("token")
                    if token is not None:
                        # Escape quotes in token to ensure valid JSON
                        escaped_token = token.replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r')
                        yield f'data: {{"token": "{escaped_token}"}}\n\n'
                        await receiver.complete_message(sb_msg)
                        
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to decode JSON from token stream message: {str(sb_msg)}, error: {e}")
                    await receiver.complete_message(sb_msg)
                except Exception as e:
                    logger.error(f"Error processing token stream message: {e}")
                    await receiver.abandon_message(sb_msg)
                    
    except Exception as e:
        logger.error(f"Error in token stream generator: {e}")
        yield f'data: {{"error": "Stream connection lost"}}\n\n'
    
    logger.info(f"SSE stream generator finished for session: {sessionId}, message: {chatMessageId}")

@app.get("/api/stream/{sessionId}/{chatMessageId}")
async def stream_tokens(sessionId: str, chatMessageId: str, request: Request):
    """
    Endpoint to stream tokens for a specific chat message via Server-Sent Events.
    
    Args:
        sessionId: The session identifier
        chatMessageId: The specific chat message identifier
    
    Returns:
        StreamingResponse: SSE stream of tokens
    """
    global sb_client
    if not sb_client:
        raise HTTPException(status_code=503, detail="Service Bus client not initialized.")

    logger.info(f"Starting SSE stream for session: {sessionId}, chatMessageId: {chatMessageId}")

    # Set up SSE headers
    headers = {
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "*",
    }

    return StreamingResponse(
        token_stream_generator(sessionId, chatMessageId), 
        media_type="text/event-stream",
        headers=headers
    )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "sse-service"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)
