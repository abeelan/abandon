import { createApp } from 'vue'
import App from './App.vue'

// 引入 element plus
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
// 注册 element plus 所有图标
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

// 引入 windicss
import 'virtual:windi.css'

// 导入通过 vue router 定义的路由
import router from './router'


// 项目运行入口
const app = createApp(App)

app.use(router)
app.use(ElementPlus)

// 注册所有图标，项目各地方使用图标的时候就不需要再挨个导入了
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.mount('#app')
