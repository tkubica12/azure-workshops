# Custom MCP Server
This demo uses Semantic Kernel and custom MCP server written in Python.

## What is the custom MCP server?

The custom MCP server (`mcp-server/main.py`) exposes tools for generating random or deterministic strings via an SSE (Server-Sent Events) interface on `localhost:8000`. It provides two main tools:
- `random_string`: Generates a random string of specified length and character types (uppercase, lowercase, digits, special characters).
- `unique_string`: Generates a deterministic string based on a seed text and character type options.

These tools can be called by the Semantic Kernel agent as part of a conversational workflow.

## How to run the custom MCP server

1. Install dependencies (from the root of this directory):
   ```
   pip install -r requirements.txt
   ```

2. Start the MCP server:
   ```
   python mcp-server/main.py
   ```

   By default, the server will listen for SSE connections on `http://localhost:8000`.

3. In another terminal, run the main assistant script as described above.

Demo questions:
- ```Ahoj, vegeneruj 5 náhodných řetězců o délce 12 znaků obsahujících jen velká písmena a
 číslice```

## Example run log

See [`output.txt`](./output.txt) for a sample session log including tool calls and assistant responses.

