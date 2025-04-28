import asyncio
from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.mcp import MCPSsePlugin
from dotenv import load_dotenv
import os
import logging

# Load environment variables from .env file
load_dotenv()

class LoggingMCPSsePlugin(MCPSsePlugin):
    async def call(self, function_name, *args, **kwargs):
        logging.info(f"Calling tool: {function_name} with args: {args}, kwargs: {kwargs}")
        result = await super().call(function_name, *args, **kwargs)
        logging.info(f"Tool {function_name} returned: {result}")
        return result

# Set up logging
logging.basicConfig(level=logging.INFO)

async def main():
    # Define random_string plugin using SSE over localhost:8000
    random_string_plugin = MCPSsePlugin(
        name="random_string",
        description="Random String Plugin",
        url="http://localhost:8000/sse",
    )
    await random_string_plugin.connect()

    # Create the kernel and add services
    kernel = Kernel()
    kernel.add_service(
        AzureChatCompletion(
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            deployment_name=os.getenv("MODEL_NAME"),
            api_version="2025-04-01-preview",
        )
    )
    kernel.add_plugin(random_string_plugin)

    agent = ChatCompletionAgent(
        kernel=kernel,
        name="SK-Assistant",
    )

    thread = ChatHistoryAgentThread()

    while True:
        user_input = input("\n🧑 User: ")
        if not user_input.strip():
            break
        response = await agent.get_response(messages=user_input, thread=thread)
        print("\n🤖 Assistant:", response.content)

    await random_string_plugin.close()

asyncio.run(main())
