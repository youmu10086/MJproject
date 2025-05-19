import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { fileURLToPath, URL } from "node:url";

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)), // 路径别名
    },
  },
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: `
          @use "@/styles/base/variables" as *;
          @use "@/styles/mixins/mixins" as *;
        `,
      },
    },
  },
  server: {
    host: "0.0.0.0",
    port: 8080, // 自定义前端端口
    proxy: {
      "/api": {
        target: "http://127.0.0.1:8000/",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  },
  build: {
    minify: "terser", // 使用 Terser 压缩代码
    terserOptions: {
      compress: {
        drop_console: true, // 移除 console 语句
        drop_debugger: true, // 移除 debugger 语句
      },
    },
  },
  optimizeDeps: {
    include: ["element-plus/es/locale/lang/zh-cn",'echarts', 'vue-echarts'],
  },
});
