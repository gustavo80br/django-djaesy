import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [vue()],
    build: {
        manifest: true, // adds a manifest.json
        rollupOptions: {
            input: [
              path.resolve(__dirname, './main.js'),
            ]
        },
        outDir:  'static', // puts the manifest.json in PROJECT_ROOT/theme/static/
        assetsDir:  'theme', // puts asset files in in PROJECT_ROOT/theme/static/theme
    },
    server: {
        port: 3000, // make sure this doesn't conflict with other ports you're using
        open: false,
    }
})
