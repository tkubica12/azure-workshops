import asyncio
from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.mcp import MCPStdioPlugin
from dotenv import load_dotenv
import os
import logging

# Load environment variables from .env file
load_dotenv()

class LoggingMCPStdioPlugin(MCPStdioPlugin):
    async def call(self, function_name, *args, **kwargs):
        logging.info(f"Calling tool: {function_name} with args: {args}, kwargs: {kwargs}")
        result = await super().call(function_name, *args, **kwargs)
        logging.info(f"Tool {function_name} returned: {result}")
        return result

# Set up logging
logging.basicConfig(level=logging.INFO)

async def main():
    # Define GitHub MCP server plugin
    github_plugin = LoggingMCPStdioPlugin(
        name="Github",
        description="Github Plugin",
        command="docker",
        args=["run", "-i", "--rm", "-e", "GITHUB_PERSONAL_ACCESS_TOKEN", "ghcr.io/github/github-mcp-server"],
        env={"GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")},
    )
    await github_plugin.connect()

    # Create the kernel and add services
    kernel = Kernel()
    kernel.add_service(
        AzureChatCompletion(
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            deployment_name=os.getenv("MODEL_NAME"),
            api_version="2025-04-01-preview",
        )
    )
    kernel.add_plugin(github_plugin)

    # Add the SSE-based MCP plugin
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

    await github_plugin.close()

asyncio.run(main())
