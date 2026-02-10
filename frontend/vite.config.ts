import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [sveltekit()],
  server: {
    proxy: {
      // Proxy all requests starting with /api to the FastAPI backend
      '/api': {
        target: 'http://localhost:8000', // Your FastAPI server
        changeOrigin: true,
      }
    }
  }
});
