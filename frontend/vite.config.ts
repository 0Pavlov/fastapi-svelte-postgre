import tailwindcss from '@tailwindcss/vite';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [tailwindcss(), sveltekit()],
  server: {
    host: true, // needed for Docker '--host'
    port: 5173,
    proxy: {
      '/api': 'http://backend:8000' // Proxy (use just /api to call / backend endpoint)
    }
  }
});
