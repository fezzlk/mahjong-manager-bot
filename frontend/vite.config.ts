import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: process.env.VITE_FLASK_URL ?? 'http://localhost:5000',
        changeOrigin: true,
      },
      '/auth': {
        target: process.env.VITE_FLASK_URL ?? 'http://localhost:5000',
        changeOrigin: true,
      },
      '/callback': {
        target: process.env.VITE_FLASK_URL ?? 'http://localhost:5000',
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: 'dist',
  },
})
