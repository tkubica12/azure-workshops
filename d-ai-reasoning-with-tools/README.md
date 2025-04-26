# Reasoning with Tools Example (o4-mini Model)

This example demonstrates how the o4-mini model can perform advanced reasoning by interacting with external tools during its thought process. The model is empowered to call a function (`get_next_item`) multiple times as needed, using the results to inform its reasoning before formulating a final response.

## Key Features

- **Tool Use During Reasoning:**  
  The model is not limited to a single tool call. It can invoke the provided function as many times as necessary, chaining calls to gather information and verify results before responding.

- **Streaming Output:**  
  Both the model's reasoning steps and function call arguments/results are streamed to the console in real time. This allows you to observe the model's internal thought process and tool interactions as they happen.

- **Detailed Reasoning:**  
  The model explains its reasoning at each step, including why it calls the tool, how it interprets results, and how it verifies the correctness of its findings.

## How It Works

1. **Prompt:**  
   The user asks the model to gather a full chain of cities to visit, requiring it to use the `get_next_item` tool and then verify the sequence in reverse.

2. **Tool Calls:**  
   The model calls `get_next_item` repeatedly, each time passing the current city and receiving the next one in the chain. It continues until it reaches the end marker (`<END>`).

3. **Verification:**  
   After collecting the chain, the model uses the tool again to verify the sequence in reverse, ensuring correctness.

4. **Streaming:**  
   - Each reasoning step is printed as soon as it is generated.
   - Function call arguments and results are displayed live.
   - The final response is streamed as the model formulates it.

## Running the Example

1. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

2. **Set environment variables:**  
   Create a `.env` file with your Azure OpenAI endpoint and model name:
   ```
   AZURE_OPENAI_ENDPOINT=your-endpoint
   MODEL_NAME=your-model-name
   ```

3. **Run the script:**
   ```
   python main.py
   ```

4. **Observe the output:**  
   Watch as the model reasons, calls the tool, verifies results, and streams its final answer.

## Purpose

This example is designed to showcase the o4-mini model's ability to:

- Integrate external tools into its reasoning process.
- Decide autonomously when and how often to use tools.
- Provide transparent, step-by-step explanations.
- Stream outputs for real-time insight into its decision-making.

Use this as a template for building more complex reasoning systems that require dynamic tool use and transparent model behavior.
