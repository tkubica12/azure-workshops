# Scalable Chat Web Client

This is a web client for a scalable chat application. It is built using modern web technologies and is designed to be lightweight and efficient.

## Features

- Real-time chat functionality with Server-Sent Events (SSE)
- Unique session and message identifiers for tracking and context
- Scalable architecture
- Responsive design for mobile and desktop

## Getting Started

1. Clone the repository.
2. Install dependencies using `npm install`.
3. Start the development server with `npm run dev`.

## Environment Configuration

- Development uses Vite's `VITE_API_URL` from `.env` file for proxying API requests (e.g., `/api/session/start`, `/api/chat`).
- Production Docker image reads `API_URL` environment variable at runtime and writes `public/env.js` for the app.

## Runtime Environment Variables

This client reads `API_URL` from two sources:

1.  **Development (Vite):** Uses the `VITE_API_URL` defined in `.env` (via `import.meta.env.VITE_API_URL`). This is used by the Vite dev server to proxy requests to the backend.
2.  **Production (Docker):** Reads `window._env_.API_URL` from `public/env.js` injected at runtime. This directly sets the API base URL for the client.

### Session Management

On load, the client makes a `POST` request to `/api/session/start` on the front service. The front service is expected to return a JSON response like `{"sessionId": "your-unique-session-id"}`. This `sessionId` is then stored in `localStorage` and included in all subsequent `/api/chat` requests.

### Message Structure

When sending a message, the client generates a unique `chatMessageId` (a random UUID). The request body to `/api/chat` is a JSON object:

```json
{
  "message": "User's typed message",
  "sessionId": "the-current-session-id",
  "chatMessageId": "a-unique-message-id"
}
```

### `public/env.js` Stub

Add a file at `public/env.js` to serve as a stub in development:

```js
// public/env.js
window._env_ = {
  API_URL: '' // unused in dev since Vite proxy uses import.meta.env.VITE_API_URL for the proxy target
};
```

Vite will serve this file as `/env.js`, and your app will load it before `main.js`. In development, `API_URL` from `window._env_` might be empty or a placeholder, as the actual API endpoint is determined by the Vite proxy configuration using `VITE_API_URL` from the `.env` file.

### Docker Runtime Injection

The Docker `entrypoint.sh` generates `/usr/share/nginx/html/env.js` inside the container:

```sh
cat <<EOF > /usr/share/nginx/html/env.js
window._env_ = {
  API_URL: "${API_URL}"
};
EOF
```

This ensures that when Nginx serves `env.js`, `window._env_.API_URL` is set to the container's `API_URL` environment variable (defaulting to `http://localhost:8000`). This `API_URL` will be the direct base URL for API calls in production.

## Debugging

-   **Dev**: Vite logs and Hot Module Replacement (HMR) in the terminal where `npm run dev` was executed.
-   **Browser**: Use browser Developer Tools (Console and Network tabs) to inspect `sessionId` generation, SSE connection, and network requests to `/api/session/start` and `/api/chat`.
-   **Docker**: Use `docker logs <container_name_or_id>` (e.g., `docker logs chat-client` if that's the container name) to view Nginx startup logs and the `env.js` injection process.

## Docker Instructions

Build the Docker image:

```bash
docker build -t scalable-chat-client .
```

Run the Docker container, providing the `API_URL` for the backend:

```bash
docker run -d -p 8080:80 -e API_URL="http://your-backend-api-url" --name chat-client scalable-chat-client
```

Access the client at `http://localhost:8080`.

This project is licensed under the MIT License. See the LICENSE file for details.