import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'
import react from '@vitejs/plugin-react'
import postcss from './postcss.config.js'

// https://vite.dev/config/
export default defineConfig({
    plugins: [react(), tailwindcss()],
    css: { postcss },
    server: {
        port: 5173,
        proxy: {
            '/api': 'http://localhost:8000',
            '/test-run': 'http://localhost:8000'
        }
    }
})