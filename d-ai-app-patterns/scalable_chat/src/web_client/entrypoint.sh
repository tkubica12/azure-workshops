#!/bin/sh
# entrypoint.sh - generate runtime environment variables for Svelte app

# # Default to development API_URL if not provided
# : "${API_URL:=http://localhost:8000}"

# Create env.js to be consumed by the client
cat <<EOF > /usr/share/nginx/html/env.js
window._env_ = {
  API_URL: "${API_URL}",
  SSE_URL: "${SSE_URL}",
  HISTORY_API_URL: "${HISTORY_API_URL}",
  MEMORY_API_URL: "${MEMORY_API_URL}"
};
EOF

# Start nginx in foreground
nginx -g 'daemon off;'
