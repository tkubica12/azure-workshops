# Random String MCP Server

This is a custom MCP (Modular Command Plugin) server that provides tools for generating random and deterministic strings. It is designed to be used with Semantic Kernel or any client that can communicate with MCP servers over Server-Sent Events (SSE).

## Features

- **random_string**: Generates a random string of specified length and character types (uppercase, lowercase, digits, special characters).
- **unique_string**: Generates a deterministic string based on a seed text and character type options.

## How it works

The server exposes its tools via SSE on `http://localhost:8000`. Clients can connect and invoke the available tools by sending requests with the required parameters.

## Usage

### 1. Install dependencies

From the root of the repository, run:
```
pip install -r ../requirements.txt
```

### 2. Start the MCP server

Run:
```
python main.py
```
The server will listen for SSE connections on `http://localhost:8000`.

### 3. Available tools

#### random_string

Generate a random string.

**Parameters:**
- `length` (int): Length of the string.
- `lower` (bool): Include lowercase letters.
- `upper` (bool): Include uppercase letters.
- `numeric` (bool): Include digits.
- `special` (bool): Include special characters.

#### unique_string

Generate a deterministic string based on a seed.

**Parameters:**
- `seed_text` (str): Seed for deterministic output.
- `length` (int): Length of the string.
- `lower` (bool): Include lowercase letters.
- `upper` (bool): Include uppercase letters.
- `numeric` (bool): Include digits.
- `special` (bool): Include special characters.

## Example

To generate 5 random strings of length 12 with uppercase letters and digits:
- Use the `random_string` tool with `length=12`, `upper=True`, `numeric=True`, `lower=False`, `special=False`.

## License

MIT License.
