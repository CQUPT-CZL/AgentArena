# AgentArena - ChatGPT 聊天应用

一个基于Vue3前端和FastAPI后端的现代化ChatGPT聊天应用。

## 🚀 项目特性

### 前端特性
- 🎨 现代化Vue3界面设计
- 💬 实时聊天体验
- 📝 支持Markdown渲染和代码高亮
- 📱 响应式设计，完美适配移动端
- ⚡ 基于Vite的快速开发体验

### 后端特性
- 🤖 集成OpenAI ChatGPT API
- 🔄 基于LangChain的智能对话管理
- 💾 多会话支持
- 🛡️ 完善的错误处理和日志记录
- 🌐 CORS支持，便于前端集成

## 📁 项目结构

```
AgentArena/
├── backend/                 # FastAPI后端服务
│   ├── main.py             # 主应用文件
│   ├── requirements.txt    # Python依赖
│   ├── .env.example       # 环境变量模板
│   └── README.md          # 后端文档
├── frontend/               # Vue3前端应用
│   ├── src/               # 源代码
│   │   ├── App.vue       # 主组件
│   │   ├── main.js       # 应用入口
│   │   ├── style.css     # 全局样式
│   │   └── services/     # API服务
│   ├── package.json      # 前端依赖
│   ├── vite.config.js    # Vite配置
│   └── README.md         # 前端文档
└── README.md              # 项目总览
```

## 🛠️ 技术栈

### 后端
- **FastAPI** - 现代化Python Web框架
- **LangChain** - AI应用开发框架
- **OpenAI API** - ChatGPT集成
- **Uvicorn** - ASGI服务器
- **Python-dotenv** - 环境变量管理

### 前端
- **Vue 3** - 渐进式JavaScript框架
- **Vite** - 下一代前端构建工具
- **Axios** - HTTP客户端
- **Marked** - Markdown解析
- **Highlight.js** - 代码高亮

## 🚀 快速开始

### 环境要求

- Python 3.8+
- Node.js 16+
- OpenAI API Key

### 1. 克隆项目

```bash
git clone <repository-url>
cd AgentArena
```

### 2. 后端设置

```bash
# 进入后端目录
cd backend

# 安装Python依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，添加你的 OPENAI_API_KEY

# 启动后端服务
python main.py
```

后端服务将在 `http://localhost:8000` 启动

### 3. 前端设置

```bash
# 打开新终端，进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端应用将在 `http://localhost:3000` 启动

### 4. 访问应用

打开浏览器访问 `http://localhost:3000`，开始与ChatGPT聊天！

## 🔧 配置说明

### 后端配置

在 `backend/.env` 文件中配置：

```env
OPENAI_API_KEY=sk-your-actual-api-key-here
PORT=8000
HOST=0.0.0.0
DEBUG=True
```

### 前端配置

前端通过Vite代理配置自动将API请求转发到后端：

```javascript
// vite.config.js
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

## 📚 API文档

后端启动后，可以访问以下地址查看API文档：

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 主要API端点

- `POST /chat` - 发送聊天消息
- `DELETE /chat/{conversation_id}` - 清除对话历史
- `GET /health` - 健康检查

## 🎯 使用指南

### 基本聊天

1. 在输入框中输入你的问题
2. 按Enter发送（Shift+Enter换行）
3. 等待ChatGPT回复
4. 支持连续对话，AI会记住上下文

### 高级功能

- **清空对话**：点击右上角的清空按钮
- **Markdown支持**：AI回复支持Markdown格式
- **代码高亮**：代码块自动语法高亮
- **响应式设计**：支持手机和平板访问

## 🔍 故障排除

### 常见问题

1. **后端启动失败**
   - 检查Python版本和依赖安装
   - 确认OpenAI API Key配置正确
   - 查看终端错误信息

2. **前端无法连接后端**
   - 确认后端服务正在运行
   - 检查端口是否被占用
   - 查看浏览器控制台错误

3. **ChatGPT响应错误**
   - 检查API Key是否有效
   - 确认网络连接正常
   - 查看后端日志

### 日志查看

- 后端日志：查看终端输出
- 前端日志：打开浏览器开发者工具

## 🚀 部署

### 开发环境

按照上述快速开始步骤即可。

### 生产环境

1. **后端部署**
   ```bash
   # 使用gunicorn部署
   pip install gunicorn
   gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

2. **前端部署**
   ```bash
   # 构建生产版本
   npm run build
   # 部署dist目录到Web服务器
   ```

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

## 🙏 致谢

- OpenAI for ChatGPT API
- LangChain for AI framework
- Vue.js and FastAPI communities
