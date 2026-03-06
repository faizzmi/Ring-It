import { fileURLToPath, URL } from 'node:url'
import tailwindcss from '@tailwindcss/vite'
import Vue from '@vitejs/plugin-vue'
import Fonts from 'unplugin-fonts/vite'
import { defineConfig } from 'vite'
import Vuetify, { transformAssetUrls } from 'vite-plugin-vuetify'

export default defineConfig({
  plugins: [
    tailwindcss(),
    Vue({
      template: { transformAssetUrls },
    }),
    Vuetify({
      autoImport: true,
      styles: {
        configFile: 'src/styles/settings.scss',
      },
    }),
    Fonts({
      fontsource: {
        families: [
          { name: 'Roboto Mono', weights: [400, 700] },
          { name: 'Roboto', weights: [100, 300, 400, 500, 700, 900], styles: ['normal', 'italic'] },
        ],
      },
    }),
  ],
  css: {
    preprocessorOptions: {
      sass: {
        api: 'legacy',
      } as any,
      scss: {
        api: 'legacy',
      } as any,
    },
    preprocessorMaxWorkers: 0,
  },
  define: { 'process.env': {} },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('src', import.meta.url)),
    },
    extensions: ['.js', '.json', '.jsx', '.mjs', '.ts', '.tsx', '.vue'],
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',  // your FastAPI port
        changeOrigin: true,
      },
    },
  },
})