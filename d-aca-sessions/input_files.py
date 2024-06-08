from langchain_azure_dynamic_sessions import SessionsPythonREPLTool
import json

tool = SessionsPythonREPLTool(
    pool_management_endpoint="https://eastus.dynamicsessions.io/subscriptions/d3b7888f-c26e-4961-a976-ff9d5b31dfd3/resourceGroups/d-aca-sessions/sessionPools/mypool",
)

upload_metadata = tool.upload_file(
    local_file_path="./people.csv", remote_file_path="important_data.json"
)

code = f"""
import csv
import statistics

# Read the data from the CSV file
with open('{upload_metadata.full_path}', 'r') as f:
    reader = csv.DictReader(f)
    ages = [int(row['Age']) for row in reader]

# Calculate the average age
statistics.mean(ages)
"""

output = tool.execute(code)
print(json.dumps(output, indent=2))
