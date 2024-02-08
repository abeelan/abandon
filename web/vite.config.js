import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// 导入 element plus 插件
// import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'

// 导入 windicss 插件
import WindiCSS from 'vite-plugin-windicss'

import path from "path"

// https://vitejs.dev/config/
export default defineConfig({
  resolve: {
    // 设置 src 目录别名，后续通过别名来使用该目录
    alias: {
      "~": path.resolve(__dirname, "src")
    }
  },
  plugins: [
    vue(),
    WindiCSS()
  ],
})
