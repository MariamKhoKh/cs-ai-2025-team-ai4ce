import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  // allow overriding base path via env (useful if you deploy under a subpath)
  base: process.env.VITE_BASE_PATH || '/',
  build: {
    outDir: 'dist' // ensure build output is "dist" for Vercel static-build
  }
})
