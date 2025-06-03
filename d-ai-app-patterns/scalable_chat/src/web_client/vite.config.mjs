import { defineConfig, loadEnv } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';

// https://vitejs.dev/config/
export default ({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '');
  return defineConfig({
    plugins: [svelte()],
    server: {
      proxy: {
        '/api': { // Changed from '/chat' to '/api' to catch all API calls
          target: env.VITE_API_URL,
          changeOrigin: true,
          secure: false,
        },
      },
    },
  });
};
