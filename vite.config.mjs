import { defineConfig } from 'vite';
import { resolve } from 'path';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({

    plugins: [
        tailwindcss(),
    ],

    base: "/static/",
    resolve: {
      alias: {
        '@': resolve('./static'),
      },
    },

    build: {
      // generate .vite/manifest.json in outDir
      manifest: "manifest.json",
      outDir: resolve("./assets"),
      assetsDir: "django-assets",
      rollupOptions: {
        input: {
            test: resolve('./static/js/main.js')
        },
      },
    },
  })