import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3000, // 你希望使用的端口号
    // strictPort: true, // 如果该端口已被占用，则会直接退出，不会尝试下一个端口
  }
})
