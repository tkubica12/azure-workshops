import os
import json
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
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
OS_ENV = os.getenv("OS_ENV", "local")

if not SERVICEBUS_FULLY_QUALIFIED_NAMESPACE or not SERVICEBUS_USER_MESSAGES_TOPIC or not SERVICEBUS_TOKEN_STREAMS_TOPIC or not SERVICEBUS_TOKEN_STREAMS_SUBSCRIPTION:
    raise RuntimeError("Missing Service Bus configuration in environment variables")

# Initialize Azure credentials and Service Bus client
credential = DefaultAzureCredential()
sb_client = ServiceBusClient(
    fully_qualified_namespace=SERVICEBUS_FULLY_QUALIFIED_NAMESPACE,
    credential=credential,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic (if any) goes here
    yield
    # Shutdown logic
    await sb_client.close()
    await credential.close()

app = FastAPI(
    title="Scalable Chat Front Service",
    version="0.1.0",
    description="Front-end for scalable chat using SSE and Azure Service Bus",
    lifespan=lifespan,
)

class ChatRequest(BaseModel):
    """
    Request model for chat API
    - session_id: Conversation session identifier
    - question: User question text
    """
    session_id: str
    question: str

@app.post("/chat")
async def chat(request: ChatRequest):
    """
    Start a new SSE stream for the given session.
    Enqueues user question to Service Bus and streams back response tokens.
    """
    # Enqueue the request message
    sender = sb_client.get_topic_sender(topic_name=SERVICEBUS_USER_MESSAGES_TOPIC)
    async with sender:
        payload = {"session_id": request.session_id, "question": request.question}
        message = ServiceBusMessage(
            json.dumps(payload), session_id=request.session_id
        )
        await sender.send_messages(message)

    async def event_generator():
        """
        Async generator that yields SSE events from Service Bus messages (token stream).
        """
        receiver = sb_client.get_subscription_receiver(
            topic_name=SERVICEBUS_TOKEN_STREAMS_TOPIC,
            subscription_name=SERVICEBUS_TOKEN_STREAMS_SUBSCRIPTION,
            session_id=request.session_id,
            prefetch_count=1,
        )
        async with receiver:
            while True:
                messages = await receiver.receive_messages(max_wait_time=10)
                if not messages:
                    continue
                for msg in messages:
                    body = msg.body.decode() if hasattr(msg.body, 'decode') else str(msg)
                    await receiver.complete_message(msg)
                    # Format as SSE data field
                    yield f"data: {body}\n\n"
                    # End on sentinel
                    if body == "__END__":
                        return

    return StreamingResponse(event_generator(), media_type="text/event-stream")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)