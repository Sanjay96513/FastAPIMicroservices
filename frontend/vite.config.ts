import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0', // Necessary for Docker container accessibility
    port: 3000,
    // Proxy API requests to the backend gateway to avoid CORS issues
    proxy: {
      '/api': {
        target: 'http://api-gateway:8000', // The Docker Compose service name for the gateway
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
})