import {
    createRouter,
    createWebHashHistory
} from 'vue-router'


// 1. 定义路由组件
import Index from "~/pages/index.vue"

// 2. 定义一些路由
const routes = [
    {path: "/", component: Index}
]

// 3. 创建路由实例并传递 `routes` 配置
const router = createRouter({
    history: createWebHashHistory(),
    routes
})

// 4. 暴露出去，去 main.js 使用
export default router