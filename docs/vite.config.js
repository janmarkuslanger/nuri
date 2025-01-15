import { defineConfig } from "vite";

export default defineConfig({
  base: "/nuri/",
  build: {
    outDir: "./dist",
    rollupOptions: {
      input: "./src/main.ts",
      output: {
        entryFileNames: "main.js",
        chunkFileNames: "chunk-[name].js",
        assetFileNames: "[name][extname]",
      },
    },
  },
});
