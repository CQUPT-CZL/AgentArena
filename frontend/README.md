# ChatGPT Frontend

基于Vue3的现代化ChatGPT聊天界面。

## 功能特性

- 🎨 现代化UI设计，响应式布局
- 💬 实时聊天体验
- 📝 支持Markdown渲染和代码高亮
- 🔄 自动滚动到最新消息
- ⌨️ 智能输入框（支持Enter发送，Shift+Enter换行）
- 🗑️ 一键清空对话历史
- 📱 移动端适配
- ⚡ 基于Vite的快速开发体验

## 技术栈

- **Vue 3** - 渐进式JavaScript框架
- **Vite** - 下一代前端构建工具
- **Axios** - HTTP客户端
- **Marked** - Markdown解析器
- **Highlight.js** - 代码语法高亮
- **@vueuse/core** - Vue组合式API工具集

## 快速开始

### 1. 安装依赖

```bash
npm install
```

### 2. 启动开发服务器

```bash
npm run dev
```

应用将在 `http://localhost:3000` 启动

### 3. 构建生产版本

```bash
npm run build
```

### 4. 预览生产版本

```bash
npm run preview
```

## 项目结构

```
frontend/
├── public/                 # 静态资源
├── src/
│   ├── components/         # Vue组件
│   ├── services/          # API服务
│   │   └── chatService.js # 聊天API服务
│   ├── App.vue           # 主应用组件
│   ├── main.js           # 应用入口
│   └── style.css         # 全局样式
├── index.html            # HTML模板
├── vite.config.js        # Vite配置
├── package.json          # 项目配置
└── README.md            # 项目文档
```

## 配置说明

### API代理配置

在 `vite.config.js` 中配置了API代理，将 `/api` 路径代理到后端服务：

```javascript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
      rewrite: (path) => path.replace(/^\/api/, '')
    }
  }
}
```

### 环境要求

- Node.js >= 16
- npm >= 7

## 开发指南

### 组件说明

- **App.vue** - 主聊天界面组件
- **chatService.js** - 封装了与后端API的通信逻辑

### 样式系统

- 使用CSS变量和现代CSS特性
- 响应式设计，支持移动端
- 平滑动画和过渡效果
- 自定义滚动条样式

### API集成

聊天服务通过 `chatService.js` 与后端通信：

```javascript
import { chatService } from './services/chatService.js'

// 发送消息
const response = await chatService.sendMessage(message, conversationId)

// 清空对话
await chatService.clearConversation(conversationId)
```

## 部署

### 开发环境

确保后端服务在 `http://localhost:8000` 运行，然后启动前端开发服务器。

### 生产环境

1. 构建项目：`npm run build`
2. 将 `dist` 目录部署到Web服务器
3. 配置反向代理将API请求转发到后端服务

## 浏览器支持

- Chrome >= 87
- Firefox >= 78
- Safari >= 14
- Edge >= 88

## 故障排除

### 常见问题

1. **无法连接到后端**
   - 检查后端服务是否启动
   - 确认API代理配置正确

2. **样式显示异常**
   - 清除浏览器缓存
   - 检查CSS文件是否正确加载

3. **消息发送失败**
   - 检查网络连接
   - 查看浏览器控制台错误信息

## 贡献指南

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request