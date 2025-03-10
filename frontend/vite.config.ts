import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    cors: {
			origin: ['https://csvanalysis.up.railway.app', 'csvanalysis.up.railway.app', 'http://localhost:5173'],
			methods: ['GET', 'POST'],
			allowedHeaders: ['Content-Type']
		},
    allowedHosts: ['https://csvanalysis.up.railway.app', 'csvanalysis.up.railway.app'],
    host: '0.0.0.0',
    port: 8080,
  },
  preview: {
    cors: {
			origin: ['https://csvanalysis.up.railway.app', 'csvanalysis.up.railway.app', 'http://localhost:5173'],
			methods: ['GET', 'POST'],
			allowedHeaders: ['Content-Type']
		},
    allowedHosts: ['https://csvanalysis.up.railway.app', 'csvanalysis.up.railway.app'],
    host: '0.0.0.0',
    port: 8080,
  },
})
