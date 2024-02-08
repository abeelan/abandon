import { createApp } from 'vue'
import App from './App.vue'

// 引入 element plus
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

// 引入 windicss
import 'virtual:windi.css'

// 导入通过 vue router 定义的路由
import router from './router'

// 项目运行入口
const app = createApp(App)

app.use(router)
app.use(ElementPlus)

app.mount('#app')
