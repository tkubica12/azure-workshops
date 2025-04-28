import asyncio
from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.mcp import MCPSsePlugin
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

async def main():
    # Create the kernel and add services
    kernel = Kernel()
    kernel.add_service(
        AzureChatCompletion(
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            deployment_name=os.getenv("MODEL_NAME"),
            api_version="2025-04-01-preview",
        )
    )

    # Add the SSE-based MCP plugin
    async with MCPSsePlugin(
        name="Azure",
        description="Azure Plugin",
        url="http://localhost:12345", 
    ) as github_plugin:
        kernel.add_plugin(github_plugin)

        agent = ChatCompletionAgent(
            kernel=kernel,
            name="SK-Assistant",
        )

        thread = ChatHistoryAgentThread()

        while True:
            user_input = input("User: ")
            if not user_input.strip():
                break
            response = await agent.get_response(messages=user_input, thread=thread)
            print("Assistant:", response.content)

asyncio.run(main())
