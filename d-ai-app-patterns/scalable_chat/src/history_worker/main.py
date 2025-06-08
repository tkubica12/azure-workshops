import os
import json
import asyncio
import logging
import signal
import sys
from datetime import datetime, timezone
from dotenv import load_dotenv
from azure.identity.aio import DefaultAzureCredential
from azure.servicebus.aio import ServiceBusClient
from azure.servicebus import ServiceBusMessage
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace
from azure.cosmos.aio import CosmosClient
from azure.cosmos import exceptions
import redis.asyncio as redis
from redis_entraid.cred_provider import create_from_default_azure_credential
from azure.ai.inference.aio import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage


# Load .env in development
load_dotenv()


# Service Bus configuration
SERVICEBUS_FULLY_QUALIFIED_NAMESPACE = os.getenv("SERVICEBUS_FULLY_QUALIFIED_NAMESPACE")
SERVICEBUS_MESSAGE_COMPLETED_TOPIC = os.getenv("SERVICEBUS_MESSAGE_COMPLETED_TOPIC")
SERVICEBUS_MESSAGE_COMPLETED_SUBSCRIPTION = os.getenv("SERVICEBUS_MESSAGE_COMPLETED_SUBSCRIPTION")
MAX_CONCURRENCY = int(os.getenv("MAX_CONCURRENCY", 10))

if not SERVICEBUS_FULLY_QUALIFIED_NAMESPACE or not SERVICEBUS_MESSAGE_COMPLETED_TOPIC or not SERVICEBUS_MESSAGE_COMPLETED_SUBSCRIPTION:
    raise RuntimeError("Missing Service Bus configuration in environment variables")

# Cosmos DB configuration
COSMOS_ENDPOINT = os.getenv("COSMOS_ENDPOINT")
COSMOS_DATABASE_NAME = os.getenv("COSMOS_DATABASE_NAME", "mydb")
COSMOS_CONTAINER_NAME = os.getenv("COSMOS_CONTAINER_NAME", "mydocuments")

if not COSMOS_ENDPOINT:
    raise RuntimeError("Missing required environment variable COSMOS_ENDPOINT")

# Redis configuration
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6380))
REDIS_SSL = os.getenv("REDIS_SSL", "true").lower() == "true"

if not REDIS_HOST:
    raise RuntimeError("Missing required environment variable REDIS_HOST")

# Azure AI Inference endpoint for title generation
AZURE_AI_CHAT_ENDPOINT = os.getenv("AZURE_AI_CHAT_ENDPOINT")
if not AZURE_AI_CHAT_ENDPOINT:
    raise RuntimeError("Missing required environment variable AZURE_AI_CHAT_ENDPOINT")

# Logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'WARNING').upper()
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)

# Azure Monitor (optional, for observability)
configure_azure_monitor(
    enable_live_metrics=True,
    instrumentation_options={
        "azure_sdk": {"enabled": True},
        "django": {"enabled": False},
        "fastapi": {"enabled": False},
        "flask": {"enabled": False},
        "psycopg2": {"enabled": False},
        "requests": {"enabled": False},
        "urllib": {"enabled": False},
        "urllib3": {"enabled": False},
    }
)
tracer = trace.get_tracer(__name__)

# Shared Azure credentials
shared_credential = DefaultAzureCredential(exclude_interactive_browser_credential=False)

# Global clients - will be initialized in main()
cosmos_client = None
redis_client = None
chat_client = None

# Global shutdown event for graceful shutdown
shutdown_event = asyncio.Event()


async def generate_conversation_title(conversation_data: dict) -> str:
    """
    Generate a conversation title based on the full conversation history using LLM.
    """
    try:
        messages = conversation_data.get("messages", [])
        if not messages:
            return "New Conversation"
        
        # If title already exists, return it
        if conversation_data.get("title"):
            return conversation_data["title"]
        
        # Build conversation summary for title generation
        # Take up to 6 messages (3 exchanges) to capture the conversation essence
        conversation_excerpt = []
        for i, msg in enumerate(messages[:6]):
            role = msg.get("role", "")
            content = msg.get("content", "")
            if role == "user":
                conversation_excerpt.append(f"User: {content[:150]}")
            elif role == "assistant":
                conversation_excerpt.append(f"Assistant: {content[:150]}")
        
        if not conversation_excerpt:
            return "New Conversation"
        
        conversation_text = "\n".join(conversation_excerpt)
        
        # Generate title using LLM with full conversation context
        title_prompt = [
            SystemMessage("You are a helpful assistant that generates concise conversation titles. Analyze the conversation and generate a short, descriptive title (3-6 words) that captures the main topic or theme. Do not use quotes or special characters. Return only the title."),
            UserMessage(f"Generate a descriptive title for this conversation:\n\n{conversation_text}")
        ]
        
        completion = await chat_client.complete(messages=title_prompt, max_tokens=25, temperature=0.3)
        generated_title = completion.choices[0].message.content.strip()
        
        # Clean up the title
        generated_title = generated_title.replace('"', '').replace("'", '').replace(':', '')
        if len(generated_title) > 50:
            generated_title = generated_title[:50].strip()
        
        # Ensure title is not empty after cleanup
        if not generated_title:
            generated_title = "New Conversation"
        
        logger.info(f"Generated title: '{generated_title}' for session {conversation_data.get('sessionId')} based on {len(messages)} messages")
        return generated_title
        
    except Exception as e:
        # For any errors, log and return fallback
        # Don't fail the entire conversation persistence for title generation
        logger.warning(f"Error generating conversation title, using fallback: {e}")
        return "New Conversation"


async def fetch_conversation_from_redis(session_id: str) -> dict:
    """
    Fetch conversation data from Redis.
    """
    try:
        redis_key = f"session:{session_id}"
        conversation_data = await redis_client.get(redis_key)
        
        if not conversation_data:
            logger.warning(f"No conversation data found in Redis for session {session_id}")
            return None
        
        conversation = json.loads(conversation_data)
        logger.info(f"Retrieved conversation data from Redis for session {session_id} with {len(conversation.get('messages', []))} messages")
        return conversation
        
    except Exception as e:
        logger.error(f"Error fetching conversation from Redis for session {session_id}: {e}")
        raise


async def persist_conversation_to_cosmos(conversation_data: dict):
    """
    Persist conversation data to Cosmos DB.
    """
    # Ensure required fields
    session_id = conversation_data.get("sessionId")
    user_id = conversation_data.get("userId")
    
    if not session_id or not user_id:
        logger.error(f"Missing required fields in conversation data: sessionId={session_id}, userId={user_id}")
        raise ValueError(f"Missing required fields in conversation data: sessionId={session_id}, userId={user_id}")
    
    # Generate title if not present
    if not conversation_data.get("title"):
        conversation_data["title"] = await generate_conversation_title(conversation_data)
    # Prepare document for Cosmos DB
    cosmos_document = {
        "id": session_id, 
        "sessionId": session_id,
        "userId": user_id, 
        "title": conversation_data.get("title"),
        "createdAt": conversation_data.get("createdAt"),
        "lastActivity": conversation_data.get("lastActivity"),
        "messages": conversation_data.get("messages", []),
        "persistedAt": datetime.now(timezone.utc).isoformat()
    }
    # Get container reference
    database = cosmos_client.get_database_client(COSMOS_DATABASE_NAME)
    container = database.get_container_client(COSMOS_CONTAINER_NAME)
    
    # Upsert document with simple retry on 429 throttling
    max_retries = 3
    for attempt in range(max_retries):
        try:
            await container.upsert_item(body=cosmos_document)
            break  # Success, exit retry loop
        except exceptions.CosmosHttpResponseError as e:
            if e.status_code == 429 and attempt < max_retries - 1:
                # Throttling, wait and retry
                wait_time = (attempt + 1) * 2  # 2, 4, 6 seconds
                logger.warning(f"Cosmos DB throttled (429), retrying in {wait_time} seconds (attempt {attempt + 1})")
                await asyncio.sleep(wait_time)
                continue
            else:
                # Other Cosmos errors or max retries exceeded
                raise
    
    logger.info(f"Successfully persisted conversation {session_id} to Cosmos DB with title: '{cosmos_document['title']}'")


async def process_message_completed_event(sb_client: ServiceBusClient, service_bus_message):
    """
    Process a message-completed event: fetch conversation from Redis and persist to Cosmos DB.
    """
    try:
        message_body_str = str(service_bus_message)
        logger.info(f"Received message-completed event: {message_body_str}")
        message_data = json.loads(message_body_str)
        
        session_id = message_data.get("sessionId")
        user_id = message_data.get("userId")
        chat_message_id = message_data.get("chatMessageId")
        
        if not session_id:
            logger.error(f"Message missing required sessionId: {message_data}")
            raise ValueError(f"Message missing required sessionId: {message_data}")
        
        logger.info(f"Processing message-completed event for session {session_id}, user {user_id}, chatMessage {chat_message_id}")
        
        # Fetch conversation data from Redis
        conversation_data = await fetch_conversation_from_redis(session_id)
        
        if not conversation_data:
            logger.warning(f"Could not fetch conversation data for session {session_id}")
            raise Exception(f"Could not fetch conversation data for session {session_id}")
        
        # Persist to Cosmos DB
        await persist_conversation_to_cosmos(conversation_data)
        logger.info(f"Successfully processed message-completed event for session {session_id}")
        
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing message body as JSON: {e}")
        raise
    except Exception as e:
        logger.error(f"Error processing message-completed event: {e}")
        raise


async def _process_and_handle_message(sb_client: ServiceBusClient, msg: ServiceBusMessage, receiver, semaphore: asyncio.Semaphore, logger_instance: logging.Logger):
    """
    Process a message, settle it, and release the concurrency semaphore.
    Simple approach: abandon any error so another worker can try.
    """
    async with semaphore:
        try:
            # Check for shutdown before processing
            if shutdown_event.is_set():
                logger_instance.info("Shutdown event set, abandoning message")
                await receiver.abandon_message(msg)
                return
            
            # Process the message
            await process_message_completed_event(sb_client, msg)
            
            # Complete the message if processing was successful
            await receiver.complete_message(msg)
            logger_instance.debug(f"Message {msg.message_id} completed successfully")
            
        except Exception as e:
            logger_instance.error(f"Error processing message {msg.message_id}: {e}")
            
            try:
                # Abandon all errors so another worker can try
                await receiver.abandon_message(msg)
                logger_instance.warning(f"Message {msg.message_id} abandoned for another worker to try")
                    
            except Exception as settle_error:
                logger_instance.error(f"Error settling message {msg.message_id}: {settle_error}")
                # If we can't settle the message, it will be retried automatically


async def setup_signal_handlers():
    """
    Setup signal handlers for graceful shutdown using asyncio.
    """
    def signal_handler(signum, frame):
        logger.info(f"Received signal {signum}, initiating graceful shutdown...")
        shutdown_event.set()
    
    # Register signal handlers
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)


async def wait_for_tasks_completion(active_tasks: set, timeout: int = 60):
    """
    Wait for all active tasks to complete or timeout.
    """
    if not active_tasks:
        return
    
    logger.info(f"Waiting for {len(active_tasks)} active tasks to complete...")
    
    try:
        await asyncio.wait_for(asyncio.gather(*active_tasks, return_exceptions=True), timeout=timeout)
        logger.info("All active tasks completed successfully")
    except asyncio.TimeoutError:
        logger.warning(f"Timeout waiting for tasks to complete after {timeout} seconds")
        # Cancel remaining tasks
        for task in active_tasks:
            if not task.done():
                task.cancel()
        # Wait briefly for cancellation to take effect
        await asyncio.gather(*active_tasks, return_exceptions=True)


async def main():
    global cosmos_client, redis_client, chat_client
    logger.info("Starting History Worker...")
    logger.info(f"Service Bus Namespace: {SERVICEBUS_FULLY_QUALIFIED_NAMESPACE}")
    logger.info(f"Listening for message-completed events on Topic: '{SERVICEBUS_MESSAGE_COMPLETED_TOPIC}', Subscription: '{SERVICEBUS_MESSAGE_COMPLETED_SUBSCRIPTION}'")
    logger.info(f"Cosmos DB Endpoint: {COSMOS_ENDPOINT}")
    logger.info(f"Cosmos Database: {COSMOS_DATABASE_NAME}, Container: {COSMOS_CONTAINER_NAME}")
    logger.info(f"Maximum concurrency for message processing: {MAX_CONCURRENCY}")
    logger.info(f"Redis Host: {REDIS_HOST}:{REDIS_PORT}, SSL: {REDIS_SSL}")
    
    # Setup signal handlers for graceful shutdown
    await setup_signal_handlers()
    
    # Initialize Cosmos DB client
    try:
        cosmos_client = CosmosClient(COSMOS_ENDPOINT, credential=shared_credential)
        logger.info("Cosmos DB client initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Cosmos DB client: {e}")
        raise
    
    # Initialize the Redis client with managed identity authentication
    try:
        redis_credential_provider = create_from_default_azure_credential(
            ("https://redis.azure.com/.default",)
        )
        
        redis_client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            ssl=REDIS_SSL,
            ssl_cert_reqs=None,  # For Azure Managed Redis, SSL cert validation can be relaxed
            credential_provider=redis_credential_provider
        )
        
        await redis_client.ping()
        logger.info("Redis connection established successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize Redis client: {e}")
        raise
    
    # Initialize the chat client for title generation
    try:
        chat_client = ChatCompletionsClient(
            endpoint=AZURE_AI_CHAT_ENDPOINT,
            credential=shared_credential,
            credential_scopes=["https://cognitiveservices.azure.com/.default"]
        )
        logger.info("Azure AI Chat client initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Azure AI Chat client: {e}")
        raise
    
    credential = DefaultAzureCredential()
    semaphore = asyncio.Semaphore(MAX_CONCURRENCY)
    active_tasks = set()
    
    try:
        while not shutdown_event.is_set():
            try:
                async with ServiceBusClient(
                    fully_qualified_namespace=SERVICEBUS_FULLY_QUALIFIED_NAMESPACE,
                    credential=credential
                ) as sb_client:
                    
                    logger.info(f"Connected to Service Bus, listening for messages on topic '{SERVICEBUS_MESSAGE_COMPLETED_TOPIC}', subscription '{SERVICEBUS_MESSAGE_COMPLETED_SUBSCRIPTION}'")
                    
                    async with sb_client.get_subscription_receiver(
                        topic_name=SERVICEBUS_MESSAGE_COMPLETED_TOPIC,
                        subscription_name=SERVICEBUS_MESSAGE_COMPLETED_SUBSCRIPTION,
                        max_wait_time=30
                    ) as receiver:
                        
                        async for msg in receiver:
                            # Check for shutdown
                            if shutdown_event.is_set():
                                logger.info("Shutdown event set, stopping message reception")
                                await receiver.abandon_message(msg)
                                break
                            
                            # Create a task to process the message
                            task = asyncio.create_task(
                                _process_and_handle_message(sb_client, msg, receiver, semaphore, logger)
                            )
                            active_tasks.add(task)
                            
                            # Remove completed tasks from the set
                            active_tasks = {t for t in active_tasks if not t.done()}
                            
                            logger.debug(f"Active tasks count: {len(active_tasks)}")
                            
            except Exception as e:
                if shutdown_event.is_set():
                    logger.info("Shutdown initiated, stopping message processing")
                    break
                logger.error(f"Error in main message loop: {e}")
                logger.info("Retrying in 5 seconds...")
                await asyncio.sleep(5)
    
    finally:
        logger.info("Shutting down History Worker...")
        
        # Wait for active tasks to complete
        await wait_for_tasks_completion(active_tasks, timeout=60)
        
        # Close clients
        try:
            if redis_client:
                await redis_client.aclose()
                logger.info("Redis client closed")
        except Exception as e:
            logger.error(f"Error closing Redis client: {e}")
        
        try:
            if cosmos_client:
                await cosmos_client.close()
                logger.info("Cosmos DB client closed")
        except Exception as e:
            logger.error(f"Error closing Cosmos DB client: {e}")
        
        logger.info("History Worker shutdown complete")


if __name__ == "__main__":
    asyncio.run(main())
