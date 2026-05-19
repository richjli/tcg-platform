import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/cards': 'http://localhost:8000',
      '/prices': 'http://localhost:8000',
      '/alerts': 'http://localhost:8000',
    },
  },
})
