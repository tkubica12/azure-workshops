from langchain_openai import AzureChatOpenAI
from browser_use import Agent
from pydantic import SecretStr
from dotenv import load_dotenv
import os

load_dotenv()

import asyncio

llm = AzureChatOpenAI(
    model="gpt-4o",
    api_version='2024-10-21',
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT', ''),
    api_key=SecretStr(os.getenv('AZURE_OPENAI_KEY', '')),
)

async def main():
    agent = Agent(
        task="Je v Baumaxu na prodejně v Letňanech dostupný krumpáč skladem? Pokud ano, lze při platbě uplatnit slevový kód JARO10?",
        llm=llm,
        use_vision=True, 
    )
    result = await agent.run()
    print(result)

asyncio.run(main())