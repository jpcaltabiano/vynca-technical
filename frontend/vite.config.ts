import { defineConfig } from 'vite'
import tsconfigPaths from 'vite-tsconfig-paths'
export default defineConfig({
  plugins:[
    tsconfigPaths()
  ],
  server: {
    proxy: {
      '/graphql': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false
      }
    }
  }
});