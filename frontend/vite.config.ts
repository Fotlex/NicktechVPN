import { defineConfig, loadEnv } from "vite";
import vue from '@vitejs/plugin-vue';
import vueDevTools from 'vite-plugin-vue-devtools';
import { createSvgIconsPlugin } from 'vite-plugin-svg-icons';
import path from 'path';

export default defineConfig(({ mode }) => { 
  
  const env = loadEnv(mode, process.cwd(), "");

  return {
    plugins: [
      vue(),
      vueDevTools(),
      createSvgIconsPlugin({
        iconDirs: [path.resolve(process.cwd(), 'src/assets/icons')],
        symbolId: 'icon-[dir]-[name]',
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