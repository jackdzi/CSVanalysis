import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    allowedHosts: ['csvanalysis.up.railway.app'],
    host: '0.0.0.0',
    port: 8080,
  },
  preview: {
    allowedHosts: ['csvanalysis.up.railway.app'],
    host: '0.0.0.0',
    port: 8080,
  },
})
