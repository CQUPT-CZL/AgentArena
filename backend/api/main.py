from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from core.logging import logger
from models import ChatMessage, ChatResponse, AgentInfo
from agents import agent_manager

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.VERSION
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据模型已从models模块导入

@app.get("/")
async def root():
    return {"message": "AgentArena API服务正在运行", "available_agents": len(agent_manager.agents)}

@app.get("/agents", response_model=List[AgentInfo])
async def get_agents():
    """获取所有可用的agent列表"""
    try:
        agents = agent_manager.get_available_agents()
        return agents
    except Exception as e:
        logger.error(f"获取agent列表错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取agent列表失败: {str(e)}")

@app.post("/chat", response_model=ChatResponse)
async def chat(chat_message: ChatMessage):
    """发送消息到指定agent"""
    try:
        # 验证agent是否存在
        if not agent_manager.get_agent(chat_message.agent_name):
            raise HTTPException(status_code=400, detail=f"Agent '{chat_message.agent_name}' 不存在")
        
        # 使用指定agent处理消息
        response = await agent_manager.process_message(
            agent_name=chat_message.agent_name,
            message=chat_message.message,
            conversation_id=chat_message.conversation_id
        )
        
        logger.info(f"Agent {chat_message.agent_name} 对话 {chat_message.conversation_id}: 用户: {chat_message.message[:50]}... AI: {response[:50]}...")
        
        return ChatResponse(
            response=response,
            agent_name=chat_message.agent_name,
            conversation_id=chat_message.conversation_id
        )
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        logger.error(f"聊天错误: {str(e)}")
        logger.error(f"错误详情: {error_details}")
        raise HTTPException(status_code=500, detail=f"聊天服务错误: {str(e)}")

@app.delete("/chat/{agent_name}/{conversation_id}")
async def clear_conversation(agent_name: str, conversation_id: str):
    """清除指定agent的对话历史"""
    try:
        success = agent_manager.clear_conversation(agent_name, conversation_id)
        if success:
            return {"message": f"Agent {agent_name} 的对话 {conversation_id} 已清除"}
        else:
            return {"message": "对话不存在或agent不存在"}
    except Exception as e:
        logger.error(f"清除对话错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"清除对话失败: {str(e)}")

@app.get("/stats")
async def get_stats():
    """获取所有agent的统计信息"""
    try:
        stats = agent_manager.get_agent_stats()
        return stats
    except Exception as e:
        logger.error(f"获取统计信息错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取统计信息失败: {str(e)}")

@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {"status": "healthy", "service": "AgentArena API", "agents_count": len(agent_manager.agents)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)