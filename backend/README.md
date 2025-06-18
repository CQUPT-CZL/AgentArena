# ChatGPT Backend API

基于FastAPI和LangChain的ChatGPT聊天后端服务。

## 功能特性

- 🤖 集成OpenAI ChatGPT API
- 💬 支持多对话会话管理
- 🔄 异步处理，高性能
- 📝 完整的对话历史记录
- 🛡️ 错误处理和日志记录
- 🌐 CORS支持，便于前端集成

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env` 并填入你的OpenAI API Key：

```bash
cp .env.example .env
```

编辑 `.env` 文件：
```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

### 3. 启动服务

```bash
python main.py
```

或使用uvicorn：
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API接口

### 发送聊天消息

**POST** `/chat`

请求体：
```json
{
  "message": "你好，ChatGPT！",
  "conversation_id": "user123"
}
```

响应：
```json
{
  "response": "你好！我是ChatGPT，很高兴为你服务！",
  "conversation_id": "user123"
}
```

### 清除对话历史

**DELETE** `/chat/{conversation_id}`

### 健康检查

**GET** `/health`

## 项目结构

```
backend/
├── main.py              # 主应用文件
├── requirements.txt     # 依赖包列表
├── .env.example        # 环境变量模板
└── README.md           # 项目文档
```

## 注意事项

- 确保你有有效的OpenAI API Key
- 生产环境建议使用数据库存储对话历史
- 可根据需要调整模型参数（temperature等）
- 建议配置日志轮转和监控