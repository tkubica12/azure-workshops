import os
import json
import asyncio
import logging
from dotenv import load_dotenv
from azure.identity.aio import DefaultAzureCredential
from azure.servicebus.aio import ServiceBusClient
from azure.servicebus import ServiceBusMessage

# Load local .env when in development
load_dotenv()

# Read configuration from environment
SERVICEBUS_FULLY_QUALIFIED_NAMESPACE = os.getenv("SERVICEBUS_FULLY_QUALIFIED_NAMESPACE")
SERVICEBUS_USER_MESSAGES_TOPIC = os.getenv("SERVICEBUS_USER_MESSAGES_TOPIC")
SERVICEBUS_USER_MESSAGES_SUBSCRIPTION = os.getenv("SERVICEBUS_USER_MESSAGES_SUBSCRIPTION")
SERVICEBUS_TOKEN_STREAMS_TOPIC = os.getenv("SERVICEBUS_TOKEN_STREAMS_TOPIC")

if not SERVICEBUS_FULLY_QUALIFIED_NAMESPACE or not SERVICEBUS_USER_MESSAGES_TOPIC or not SERVICEBUS_USER_MESSAGES_SUBSCRIPTION or not SERVICEBUS_TOKEN_STREAMS_TOPIC:
    raise RuntimeError("Missing Service Bus configuration in environment variables")

# Logging configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'WARNING').upper()
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)

async def main():
    logger.info("Starting LLM worker...")
    logger.info(f"Service Bus Namespace: {SERVICEBUS_FULLY_QUALIFIED_NAMESPACE}")
    
    # Initialize Azure credentials and Service Bus client
    credential = DefaultAzureCredential()
    sb_client = ServiceBusClient(
        fully_qualified_namespace=SERVICEBUS_FULLY_QUALIFIED_NAMESPACE,
        credential=credential,
    )

    # Receive user messages and send response tokens
    receiver = sb_client.get_subscription_receiver(
        topic_name=SERVICEBUS_USER_MESSAGES_TOPIC,
        subscription_name=SERVICEBUS_USER_MESSAGES_SUBSCRIPTION,
        prefetch_count=1,
    )
    sender = sb_client.get_topic_sender(topic_name=SERVICEBUS_TOKEN_STREAMS_TOPIC)

    # Main processing loop
    async with receiver, sender:
        while True:
            messages = await receiver.receive_messages(max_wait_time=5, max_message_count=1)
            if not messages:
                continue
            for msg in messages:
                try:
                    body = msg.body.decode() if hasattr(msg.body, 'decode') else str(msg)
                    logger.info(f"Received user message: {body}")
                    data = json.loads(body)
                    session_id = msg.session_id or data.get('session_id')

                    # Demo: send a static response character by character
                    response_text = "This is a demo response."
                    for ch in response_text:
                        token_msg = ServiceBusMessage(ch, session_id=session_id)
                        await sender.send_messages(token_msg)
                        logger.info(f"Sent token: {ch}")
                        await asyncio.sleep(1)

                    # Send end-of-stream sentinel
                    end_msg = ServiceBusMessage("__END__", session_id=session_id)
                    await sender.send_messages(end_msg)
                    logger.info(f"Sent end of stream for session {session_id}")
                finally:
                    await receiver.complete_message(msg)

    # Cleanup
    await sb_client.close()
    await credential.close()

if __name__ == "__main__":
    asyncio.run(main())
