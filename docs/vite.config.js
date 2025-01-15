import { defineConfig } from "vite";

export default defineConfig({
  build: {
    base: "/nuri/",
    outDir: "./dist",
    emptyOutDir: true,
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
