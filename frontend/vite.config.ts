import { defineConfig, loadEnv } from "vite";
import vue from "@vitejs/plugin-vue";
import path from "node:path";
import Components from "unplugin-vue-components/vite";
import Icons from "unplugin-icons/vite";
import IconsResolver from "unplugin-icons/resolver";
import { FileSystemIconLoader } from "unplugin-icons/loaders";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");

  return {
    plugins: [
      vue(),
      Components({
        dirs: ["src/components", "src/layouts"],
        extensions: ["vue"],
        deep: true,
        resolvers: [
          IconsResolver({
            prefix: "i",
            customCollections: ["local"],
          }),
        ],
      }),
      Icons({
        compiler: "vue3",
        customCollections: {
          local: FileSystemIconLoader("./src/assets/icons", (svg) =>
            svg.replace(/^<svg /, '<svg fill="currentColor" ')
          ),
        },
      }),
    ],
    resolve: {
      alias: {
        "@": path.resolve(__dirname, "./src"),
      },
    },
    server: {
      host: "0.0.0.0",
      port: 5173,
      hmr: {
        port: 80,
        protocol: "ws",
      },
      watch: {
        usePolling: true,
      },
      allowedHosts: env.VITE_ALLOWED_HOSTS?.split(",") || ["localhost"],
    },
  };
});
