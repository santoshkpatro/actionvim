import { fileURLToPath, URL } from "node:url";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import vueDevTools from "vite-plugin-vue-devtools";

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue(), vueDevTools()],
  base: "/static/",
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./web", import.meta.url)),
    },
  },
  build: {
    outDir: "static",
    rollupOptions: {
      input: {
        main: fileURLToPath(new URL("./web/main.js", import.meta.url)),
      },
      output: {
        entryFileNames: "main.js",
      },
    },
  },
});
