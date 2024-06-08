from langchain_azure_dynamic_sessions import SessionsPythonREPLTool
import json

tool = SessionsPythonREPLTool(
	pool_management_endpoint="https://eastus.dynamicsessions.io/subscriptions/d3b7888f-c26e-4961-a976-ff9d5b31dfd3/resourceGroups/d-aca-sessions/sessionPools/mypool",
)

code = """
import numpy as np
import matplotlib.pyplot as plt

# Generate values for x from -1 to 1
x = np.linspace(-1, 1, 400)

# Calculate the sine of each x value
y = np.sin(x)

# Create the plot
plt.plot(x, y)

# Add title and labels
plt.title('Plot of sin(x) from -1 to 1')
plt.xlabel('x')
plt.ylabel('sin(x)')

# Show the plot
plt.grid(True)
plt.show()
"""

result = tool.execute(code)
print(f"Output is of type {result['result']['type']} in format {result['result']['format']}")

import base64

# Get the base64 encoded data
encoded_data = result['result']['base64_data']

# Decode the data
decoded_data = base64.b64decode(encoded_data)

# Write the data to a file
with open('output.png', 'wb') as f:
    f.write(decoded_data)
