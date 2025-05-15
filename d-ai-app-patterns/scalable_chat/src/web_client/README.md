# Scalable Chat Web Client

This is a web client for a scalable chat application. It is built using modern web technologies and is designed to be lightweight and efficient.

## Features

- Real-time chat functionality
- Scalable architecture
- Responsive design for mobile and desktop

## Getting Started

1. Clone the repository.
2. Install dependencies using `npm install`.
3. Start the development server with `npm run dev`.

## Environment Configuration

- Development uses Vite's `VITE_API_URL` from `.env` file for proxying requests.
- Production Docker image reads `API_URL` environment variable at runtime and writes `env.js` for the app.

## Runtime Environment Variables

This client reads `API_URL` from two sources:

1. **Development (Vite):** Uses the `VITE_API_URL` defined in `.env` (via `import.meta.env.VITE_API_URL`).
2. **Production (Docker):** Reads `window._env_.API_URL` from `env.js` injected at runtime.

### `public/env.js` Stub

Add a file at `public/env.js` to serve as a stub in development:
```js
// public/env.js
window._env_ = {
  API_URL: '' // unused in dev since Vite proxy uses import.meta.env.VITE_API_URL
};
```
Vite will serve this file as `/env.js`, and your app will load it before `main.js`.

### Docker Runtime Injection

The Docker `entrypoint.sh` generates `/usr/share/nginx/html/env.js` inside the container:
```sh
cat <<EOF > /usr/share/nginx/html/env.js
window._env_ = {
  API_URL: "${API_URL}"
};
EOF
```
This ensures that when Nginx serves `env.js`, `window._env_.API_URL` is set to the container's `API_URL` environment variable (defaulting to `http://localhost:8000`).

## Debugging

- **Dev**: Vite logs and HMR in the terminal at `npm run dev`.
- **Browser**: Use DevTools console to inspect SSE connection and network requests.
- **Docker**: `docker logs chat-client` to view Nginx startup and env injection logs.

## Docker Instructions

1. Build the Docker image:
   ```bash
   docker build -t chat-client .
   ```

2. Run the Docker container:
   ```bash
   docker run -d -p 80:80 --name chat-client -e API_URL=http://your-api-url chat-client
   ```

3. Access the application in your browser at `http://localhost`.

## License

This project is licensed under the MIT License. See the LICENSE file for details.