# 🤖 AgentArena 多Agent架构指南

## 📋 概述

AgentArena 现在支持多个不同类型的AI助手，用户可以在前端界面中选择不同的Agent来体验不同的AI能力。

## 🏗️ 架构设计

### 后端架构

```
backend/
├── agents/                    # Agent模块
│   ├── __init__.py           # 模块初始化
│   ├── manager.py            # Agent管理器
│   ├── simple_chat/          # 简单聊天Agent
│   │   ├── __init__.py
│   │   └── agent.py
│   └── langchain_agent/      # LangChain智能Agent
│       ├── __init__.py
│       └── agent.py
├── main.py                   # FastAPI主应用
└── ...
```

### 前端架构

- **Agent选择器**: 头部的下拉菜单，用户可以选择不同的Agent
- **动态欢迎信息**: 根据选择的Agent显示不同的介绍
- **统一聊天界面**: 所有Agent共享相同的聊天UI

## 🤖 可用的Agent

### 1. 简单对话 (simple_chat)
- **功能**: 基础的ChatGPT对话功能
- **特点**: 简单直接的问答对话
- **适用场景**: 日常聊天、基础问答

### 2. 智能助手 (langchain_agent)
- **功能**: 具备工具调用能力的智能助手
- **工具能力**:
  - 🕐 获取当前时间
  - 🧮 数学计算
  - 🌤️ 天气查询（模拟）
- **特点**: 可以执行具体任务，提供实时信息
- **适用场景**: 需要工具辅助的复杂任务

## 🚀 使用方法

### 启动服务

1. **启动后端**:
   ```bash
   cd backend
   uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **启动前端**:
   ```bash
   cd frontend
   npm run dev
   ```

3. **访问应用**: 打开 http://localhost:3000

### 使用Agent

1. 在页面顶部的"选择助手"下拉菜单中选择想要使用的Agent
2. 选择后会显示该Agent的介绍信息
3. 在输入框中输入消息，不同的Agent会提供不同类型的回复
4. 切换Agent时会自动清空当前对话

## 🔧 API接口

### 获取Agent列表
```http
GET /agents
```

### 发送消息
```http
POST /chat
Content-Type: application/json

{
  "message": "用户消息",
  "agent_name": "simple_chat",
  "conversation_id": "default"
}
```

### 清除对话
```http
DELETE /chat/{agent_name}/{conversation_id}
```

### 获取统计信息
```http
GET /stats
```

## 🛠️ 添加新的Agent

### 1. 创建Agent类

在 `backend/agents/` 下创建新的文件夹，实现Agent类：

```python
class MyCustomAgent:
    def __init__(self):
        self.name = "my_agent"
        self.display_name = "我的助手"
        self.description = "自定义助手描述"
        self.conversations = {}
    
    async def process_message(self, message: str, conversation_id: str = "default") -> str:
        # 实现消息处理逻辑
        return "处理后的回复"
    
    def clear_conversation(self, conversation_id: str) -> bool:
        # 实现清除对话逻辑
        pass
    
    def get_conversation_count(self) -> int:
        # 返回对话数量
        return len(self.conversations)
```

### 2. 注册Agent

在 `backend/agents/manager.py` 的 `_initialize_agents` 方法中添加：

```python
my_agent = MyCustomAgent()
self.agents[my_agent.name] = my_agent
```

### 3. 测试

重启后端服务，新的Agent会自动出现在前端的选择列表中。

## 🎯 特性说明

### Agent隔离
- 每个Agent维护独立的对话历史
- 切换Agent不会影响其他Agent的状态
- 支持同时与多个Agent进行不同的对话

### 扩展性
- 模块化设计，易于添加新的Agent
- 统一的接口规范
- 灵活的配置管理

### 用户体验
- 直观的Agent选择界面
- 实时的Agent信息展示
- 流畅的切换体验

## 🔍 故障排除

### 常见问题

1. **Agent列表为空**
   - 检查后端服务是否正常启动
   - 查看控制台是否有错误信息

2. **Agent切换无效**
   - 确认前端和后端的连接正常
   - 检查API请求是否包含正确的agent_name

3. **LangChain Agent工具调用失败**
   - 检查环境变量配置
   - 确认依赖包安装完整

### 日志查看

- 后端日志：查看uvicorn输出
- 前端日志：打开浏览器开发者工具查看Console

## 🚀 未来扩展

可以考虑添加的Agent类型：
- 📝 文档处理Agent
- 🔍 搜索Agent
- 🎨 创意写作Agent
- 📊 数据分析Agent
- 🌐 网络爬虫Agent

每个Agent都可以有自己独特的能力和工具集！