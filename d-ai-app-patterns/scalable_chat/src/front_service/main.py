import os
import json
import logging
import asyncio
import uuid
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from azure.identity.aio import DefaultAzureCredential
from azure.servicebus.aio import ServiceBusClient
from azure.servicebus import ServiceBusMessage
from contextlib import asynccontextmanager
import uvicorn

# Load local .env when in development
load_dotenv()

# Read configuration from environment
SERVICEBUS_FULLY_QUALIFIED_NAMESPACE = os.getenv("SERVICEBUS_FULLY_QUALIFIED_NAMESPACE")
SERVICEBUS_USER_MESSAGES_TOPIC = os.getenv("SERVICEBUS_USER_MESSAGES_TOPIC")
SERVICEBUS_TOKEN_STREAMS_TOPIC = os.getenv("SERVICEBUS_TOKEN_STREAMS_TOPIC")
SERVICEBUS_TOKEN_STREAMS_SUBSCRIPTION = os.getenv("SERVICEBUS_TOKEN_STREAMS_SUBSCRIPTION")

if not SERVICEBUS_FULLY_QUALIFIED_NAMESPACE or not SERVICEBUS_USER_MESSAGES_TOPIC or not SERVICEBUS_TOKEN_STREAMS_TOPIC or not SERVICEBUS_TOKEN_STREAMS_SUBSCRIPTION:
    raise RuntimeError("Missing Service Bus configuration in environment variables")

# Logging configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'WARNING').upper()
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)

# Initialize Azure credentials
credential = DefaultAzureCredential()

# Global ServiceBusClient
sb_client: ServiceBusClient | None = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global sb_client
    logger.info("Application startup: Initializing Service Bus client.")
    sb_client = ServiceBusClient(fully_qualified_namespace=SERVICEBUS_FULLY_QUALIFIED_NAMESPACE, credential=credential)
    yield
    logger.info("Application shutdown: Closing Service Bus client.")
    if sb_client:
        await sb_client.close()
    await credential.close()

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

class ChatMessage(BaseModel):
    message: str
    sessionId: str
    chatMessageId: str

class SessionStartResponse(BaseModel):
    sessionId: str

@app.post("/api/session/start", response_model=SessionStartResponse)
async def start_session():
    sessionId = str(uuid.uuid4())
    logger.info(f"New session started: {sessionId}")
    return SessionStartResponse(sessionId=sessionId)

async def token_stream_generator(sessionId: str, initial_chatMessageId: str):
    logger.info(f"Opening sessionful receiver for token streams for session: {sessionId}")
    async with sb_client.get_subscription_receiver(
        SERVICEBUS_TOKEN_STREAMS_TOPIC,
        SERVICEBUS_TOKEN_STREAMS_SUBSCRIPTION,
        session_id=sessionId
    ) as receiver:
        logger.info(f"Token stream receiver opened for session: {sessionId}")
        async for sb_msg in receiver:
            logger.debug(f"Received chunk: {sb_msg}")
            data = json.loads(str(sb_msg))
            # Only process tokens for the matching chatMessageId
            if data.get("chatMessageId") != initial_chatMessageId:
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
                yield f"data: {{\"token\": \"{token}\"}}\n\n"
                await receiver.complete_message(sb_msg)
    logger.info(f"SSE stream generator finished for session: {sessionId}, message: {initial_chatMessageId}")

@app.post("/api/chat")
async def chat_endpoint(chat_message: ChatMessage, request: Request):
    global sb_client
    if not sb_client:
        raise HTTPException(status_code=503, detail="Service Bus client not initialized.")

    logger.info(f"Received message: '{chat_message.message}' for session: {chat_message.sessionId}, chatMessageId: {chat_message.chatMessageId}")

    try:
        async with sb_client.get_topic_sender(SERVICEBUS_USER_MESSAGES_TOPIC) as sender:
            message_to_send = ServiceBusMessage(
                body=json.dumps({
                    "text": chat_message.message,
                    "sessionId": chat_message.sessionId,
                    "chatMessageId": chat_message.chatMessageId
                }),
                message_id=chat_message.chatMessageId,
                session_id=chat_message.sessionId
            )
            await sender.send_messages(message_to_send)
        logger.info(f"Message {chat_message.chatMessageId} for session {chat_message.sessionId} sent to topic '{SERVICEBUS_USER_MESSAGES_TOPIC}'")
    except Exception as e:
        logger.error(f"Failed to send message to Service Bus for session {chat_message.sessionId}, chatMessageId {chat_message.chatMessageId}: {e}")
        raise HTTPException(status_code=500, detail="Failed to process message.")

    return StreamingResponse(token_stream_generator(chat_message.sessionId, chat_message.chatMessageId), media_type="text/event-stream")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)