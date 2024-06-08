from langchain_azure_dynamic_sessions import SessionsPythonREPLTool
import json

tool = SessionsPythonREPLTool(
	pool_management_endpoint="https://eastus.dynamicsessions.io/subscriptions/d3b7888f-c26e-4961-a976-ff9d5b31dfd3/resourceGroups/d-aca-sessions/sessionPools/mypool",
)

code = """
# Comments are ignored

a = 5
b = 8
x = a*b

# Whatever gets printed to stdout is captured
print(f"Answer is {x}")

# Last expression is returned as the output
x
"""

output = tool.execute(code)
print(json.dumps(output, indent=2))
