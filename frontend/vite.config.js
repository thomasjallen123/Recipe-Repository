import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'  // ← THIS LINE IS REQUIRED

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')  // ← THIS IS THE MAGIC LINE
    }
  },
  server: {
    port: 3000,
    open: true
  }
})