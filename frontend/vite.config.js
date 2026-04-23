import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  const devApiTarget = env.VITE_DEV_API_TARGET
  const proxy = devApiTarget
    ? {
        '/api': {
          target: devApiTarget,
          changeOrigin: true
        },
        '/uploads': {
          target: devApiTarget,
          changeOrigin: true
        }
      }
    : undefined

  return {
    plugins: [vue()],
    base: './',
    build: {
      outDir: 'dist',
      emptyOutDir: true,
      reportCompressedSize: false,
      sourcemap: false,
      chunkSizeWarningLimit: 1600,
      rollupOptions: {
        maxParallelFileOps: 2,
        output: {
          manualChunks(id) {
            if (!id.includes('node_modules')) return undefined
            if (id.includes('element-plus')) return 'element-plus'
            if (id.includes('echarts')) return 'echarts'
            if (id.includes('vue') || id.includes('pinia')) return 'vue-vendor'
            return 'vendor'
          }
        }
      }
    },
    server: {
      host: '0.0.0.0',
      port: 5173,
      proxy
    }
  }
})
