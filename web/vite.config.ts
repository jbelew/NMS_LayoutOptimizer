import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [react(), tailwindcss()],
  build: {
    minify: 'esbuild', // Default option, optimized for speed
    cssCodeSplit: true, // Ensures CSS is split for better optimization
    rollupOptions: {
      output: {
        assetFileNames: (assetInfo) => {
          if (assetInfo.name?.endsWith('.css')) {
            return 'assets/[name]-[hash].css'; // Custom CSS output pattern
          }
          return 'assets/[name]-[hash].[ext]';
        }
      }
    },
    cssMinify: 'lightningcss'
  }
});