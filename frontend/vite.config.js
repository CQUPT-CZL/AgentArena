// frontend/vite.config.js
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      },
      '/agents': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/chat': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})