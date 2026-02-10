import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  plugins: [sveltekit(), tailwindcss()],
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
