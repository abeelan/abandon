## 环境搭建

### 安装 node
所有的环境都是基于此。
```bash
$ brew install node
```


### 安装包管理器 yarn
跟 npm 类似，速度快。
```bash
# 安装 yarn
$ npm install --global yarn
$ yarn --version
1.22.21
```

基本命令

```bash
# 在项目根目录 生成一个 package.json 文件
$ yarn init

# 单个包操作
$ yarn add [package]
$ yarn upgrade [package]
$ yarn remove [package]

# 安装项目全部依赖
$ yarn 
$ yarn install
```



### 安装构建工具 vite 

是一个 web 开发工具，可以快速构建 VUE 项目，打包。优点多多：

- 快速的冷启动
- 即时的模块热更新
- 真正的按需编译

初始化项目，创建一个 web 项目

```bash
$ yarn create vite
# 自定义项目名称
# 选择 VUE
# 选择 js
```

进入项目目录内，进行初始化 yarn 配置并安装所有依

```bash
$ yarn init
$ yarn 

# 访问前端地址
$ yarn dev
  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

脚手架文件介绍

- public: 静态资源文件
- src：
    - assets：静态资源
    - componets：组件

- app.vue：主组件，构建、定义页面组件
- main.js：这是程序运行入口，引入 app.vue 主组件展示
- index.html 最终构建的页面，里面 id 定义为 app，绑订 main.js 内的 APP，完成页面渲染。


### 需要安装的插件

- volar：vue 文件的语法提示及高亮
- Vue 3 Snippets 语法提示



### 安装组件库 element plus
[官网地址](https://element-plus.org/zh-CN/guide/quickstart.html#%E6%8C%89%E9%9C%80%E5%AF%BC%E5%85%A5)
```bash
$ yarn add element-plus

# 自动导入插件
yarn add -D unplugin-vue-components unplugin-auto-import
```

### windicss
css 样式封装。
[官方文档](https://cn.windicss.org/integrations/vite.html#install)
```bash
$ npm i -D vite-plugin-windicss windicss

安装插件：Windi CSS Intellisense
```

### vue router
[官网](https://router.vuejs.org/zh/installation.html)
```bash
$ yarn add vue-router@4
```