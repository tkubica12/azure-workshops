from langchain import hub
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_azure_dynamic_sessions import SessionsPythonREPLTool
from langchain_openai import AzureChatOpenAI
import dotenv

dotenv.load_dotenv()

llm = AzureChatOpenAI(model="gpt-4o", temperature=0, verbose=True)
prompt = hub.pull("hwchase17/openai-functions-agent")

tool = SessionsPythonREPLTool(
    pool_management_endpoint="https://eastus.dynamicsessions.io/subscriptions/d3b7888f-c26e-4961-a976-ff9d5b31dfd3/resourceGroups/d-aca-sessions/sessionPools/mypool",
)

agent = create_tool_calling_agent(llm, [tool], prompt)
agent_executor = AgentExecutor(
    agent=agent, tools=[tool], verbose=True, handle_parsing_errors=True
)

response = agent_executor.invoke(
    {
        "input": "what's sin of pi . if it's negative generate a random number between 0 and 5. if it's positive between 5 and 10."
    }
)
