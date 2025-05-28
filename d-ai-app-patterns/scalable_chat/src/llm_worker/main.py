import os
import json
import asyncio
import logging
from dotenv import load_dotenv
from azure.identity.aio import DefaultAzureCredential
from azure.servicebus.aio import ServiceBusClient
from azure.servicebus import ServiceBusMessage
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace
from azure.ai.inference.aio import ChatCompletionsClient  # async client for streaming
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.pipeline.transport import AioHttpTransport # Existing import


# Load .env in development
load_dotenv()


# Service Bus and concurrency configuration
SERVICEBUS_FULLY_QUALIFIED_NAMESPACE = os.getenv("SERVICEBUS_FULLY_QUALIFIED_NAMESPACE")
SERVICEBUS_USER_MESSAGES_TOPIC = os.getenv("SERVICEBUS_USER_MESSAGES_TOPIC")
SERVICEBUS_USER_MESSAGES_SUBSCRIPTION = os.getenv("SERVICEBUS_USER_MESSAGES_SUBSCRIPTION")
SERVICEBUS_TOKEN_STREAMS_TOPIC = os.getenv("SERVICEBUS_TOKEN_STREAMS_TOPIC")
MAX_CONCURRENCY = int(os.getenv("MAX_CONCURRENCY", 10))


if not SERVICEBUS_FULLY_QUALIFIED_NAMESPACE or not SERVICEBUS_USER_MESSAGES_TOPIC or not SERVICEBUS_USER_MESSAGES_SUBSCRIPTION or not SERVICEBUS_TOKEN_STREAMS_TOPIC:
    raise RuntimeError("Missing Service Bus configuration in environment variables")


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


# Azure AI Inference endpoint
AZURE_AI_CHAT_ENDPOINT = os.getenv("AZURE_AI_CHAT_ENDPOINT")
if not AZURE_AI_CHAT_ENDPOINT:
    raise RuntimeError("Missing required environment variable AZURE_AI_CHAT_ENDPOINT")


# Shared Azure credentials and LLM client
shared_credential = DefaultAzureCredential(exclude_interactive_browser_credential=False)
chat_client = ChatCompletionsClient(
    endpoint=AZURE_AI_CHAT_ENDPOINT,
    credential=shared_credential,
    credential_scopes=["https://cognitiveservices.azure.com/.default"],
    transport=AioHttpTransport(retries=3)
)

async def process_message(sb_client: ServiceBusClient, service_bus_message):
    """
    Handle a single user message: parse, call LLM, and stream tokens to the token streams topic.
    """
    try:
        message_body_str = str(service_bus_message)
        logger.info(f"Received message: {message_body_str}")
        
        message_data = json.loads(message_body_str)
        
        user_text = message_data.get("text")
        session_id = message_data.get("sessionId")
        chat_message_id = message_data.get("chatMessageId")

        if not all([user_text, session_id, chat_message_id]):
            logger.error(f"Message missing required fields (text, sessionId, chatMessageId): {message_data}")
            # Depending on requirements, might dead-letter this message
            return
        logger.info(f"Processing chatMessageId: {chat_message_id} for sessionId: {session_id} - Text: '{user_text}'")

        # Call Azure AI Inference SDK for chat completions with streaming
        messages = [
            SystemMessage("You are a helpful assistant."),
            UserMessage(user_text)
        ]
        stream = await chat_client.complete(stream=True, messages=messages)
        async with sb_client.get_topic_sender(SERVICEBUS_TOKEN_STREAMS_TOPIC) as sender:
            async for update in stream:
                if update.choices and update.choices[0].delta and update.choices[0].delta.content:
                    chunk = update.choices[0].delta.content
                    token_payload = {
                        "sessionId": session_id,
                        "chatMessageId": chat_message_id,
                        "token": chunk
                    }
                    token_message = ServiceBusMessage(
                        body=json.dumps(token_payload),
                        session_id=session_id
                    )
                    await sender.send_messages(token_message)
                    logger.debug(f"Sent token chunk: {chunk}")
                if update.usage:
                    logger.info(f"Token usage: {update.usage}")
            # Send end-of-stream sentinel
            eos_payload = {"sessionId": session_id, "chatMessageId": chat_message_id, "end_of_stream": True}
            eos_message = ServiceBusMessage(body=json.dumps(eos_payload), session_id=session_id)
            await sender.send_messages(eos_message)
            logger.info(f"Sent end-of-stream for chatMessageId {chat_message_id}")

    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode JSON from user message: {message_body_str}, error: {e}")
        # Potentially dead-letter the message
    except Exception as e:
        logger.error(f"Error processing message (id: {service_bus_message.message_id if service_bus_message else 'N/A'}): {e}")
        # Potentially re-raise or handle to allow the message to be abandoned/dead-lettered by the caller
        raise

async def _process_and_handle_message(sb_client: ServiceBusClient, msg: ServiceBusMessage, receiver, semaphore: asyncio.Semaphore, logger_instance: logging.Logger):
    """
    Process a message, settle it, and release the concurrency semaphore.
    """
    try:
        await process_message(sb_client, msg)
        await receiver.complete_message(msg) # Reverted to use receiver.complete_message()
        logger_instance.info(f"Successfully processed and completed message id: {msg.message_id}")
    except Exception as e:
        logger_instance.error(f"Unhandled exception during message processing for msg_id {msg.message_id}. Error: {e}. Abandoning message.")
        try:
            await receiver.abandon_message(msg) # Reverted to use receiver.abandon_message()
        except Exception as abandon_e:
            logger_instance.error(f"Failed to abandon message {msg.message_id}. Error: {abandon_e}")
    finally:
        semaphore.release()

async def main():
    logger.info("Starting LLM worker...")
    logger.info(f"Service Bus Namespace: {SERVICEBUS_FULLY_QUALIFIED_NAMESPACE}")
    logger.info(f"Listening for user messages on Topic: '{SERVICEBUS_USER_MESSAGES_TOPIC}', Subscription: '{SERVICEBUS_USER_MESSAGES_SUBSCRIPTION}'")
    logger.info(f"Sending token streams to Topic: '{SERVICEBUS_TOKEN_STREAMS_TOPIC}'")
    logger.info(f"Maximum concurrency for message processing: {MAX_CONCURRENCY}")
    
    credential = DefaultAzureCredential()
    semaphore = asyncio.Semaphore(MAX_CONCURRENCY)
    
    while True:
        active_tasks = set()
        try:
            async with ServiceBusClient(fully_qualified_namespace=SERVICEBUS_FULLY_QUALIFIED_NAMESPACE, credential=credential) as sb_client:
                async with sb_client.get_subscription_receiver(SERVICEBUS_USER_MESSAGES_TOPIC, SERVICEBUS_USER_MESSAGES_SUBSCRIPTION) as receiver:
                    logger.info("LLM Worker connected and listening for messages.")
                    async for msg in receiver:
                        await semaphore.acquire() # Wait for an available slot
                        task = asyncio.create_task(
                            _process_and_handle_message(sb_client, msg, receiver, semaphore, logger)
                        )
                        active_tasks.add(task)
                        # Remove task from set upon completion to prevent memory leak over long runs
                        task.add_done_callback(active_tasks.discard)
        except Exception as e:
            logger.error(f"Exception in LLM worker main connection/receive loop: {e}. Retrying in 10 seconds...")
            # Attempt to wait for any outstanding tasks to complete or cancel them
            # This is a simplified approach; more sophisticated shutdown might be needed for production
            if active_tasks:
                logger.info(f"Waiting for {len(active_tasks)} active tasks to complete before retrying...")
                await asyncio.wait(list(active_tasks), timeout=5.0) # Wait for a short period
            await asyncio.sleep(10) # Wait before retrying connection
        finally:
            # Ensure credential is closed if main loop exits (though this one is infinite)
            # await credential.close() # DefaultAzureCredential does not need explicit close in this async context usually
            pass 

if __name__ == "__main__":
    asyncio.run(main())
