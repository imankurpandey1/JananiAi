import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [react()],
  build: {
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes("node_modules/recharts")) return "charts";
          if (id.includes("node_modules/framer-motion")) return "motion";
          if (id.includes("node_modules/react")) return "react";
        }
      }
    }
  },
  server: {
    host: "127.0.0.1",
    port: 5173
  }
});
