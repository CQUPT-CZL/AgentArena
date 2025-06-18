from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage
import os
from dotenv import load_dotenv
from typing import List, Dict
import logging

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="ChatGPT API", description="基于LangChain的ChatGPT聊天API")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 请求模型
class ChatMessage(BaseModel):
    message: str
    conversation_id: str = "default"

class ChatResponse(BaseModel):
    response: str
    conversation_id: str

# 存储对话历史（生产环境建议使用数据库）
conversations: Dict[str, List] = {}

# 初始化ChatOpenAI
def get_chat_model():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY未设置")
    
    return ChatOpenAI(
        model="deepseek-chat",
        temperature=0.7,
        api_key=api_key,
        base_url=os.getenv("OPENAI_API_BASE"),
    )

@app.get("/")
async def root():
    return {"message": "ChatGPT API服务正在运行"}

@app.post("/chat", response_model=ChatResponse)
async def chat(chat_message: ChatMessage):
    try:
        # 获取聊天模型
        chat_model = get_chat_model()
        
        # 获取或创建对话历史
        conversation_id = chat_message.conversation_id
        if conversation_id not in conversations:
            conversations[conversation_id] = []
        
        # 添加用户消息到历史
        conversations[conversation_id].append(HumanMessage(content=chat_message.message))
        
        # 限制对话历史长度（避免token过多）
        if len(conversations[conversation_id]) > 20:
            conversations[conversation_id] = conversations[conversation_id][-20:]
        
        # 调用ChatGPT
        response = await chat_model.ainvoke(conversations[conversation_id])
        
        # 添加AI回复到历史
        conversations[conversation_id].append(AIMessage(content=response.content))
        
        logger.info(f"对话 {conversation_id}: 用户: {chat_message.message[:50]}... AI: {response.content[:50]}...")
        
        return ChatResponse(
            response=response.content,
            conversation_id=conversation_id
        )
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        logger.error(f"聊天错误: {str(e)}")
        logger.error(f"错误详情: {error_details}")
        raise HTTPException(status_code=500, detail=f"聊天服务错误: {str(e)}")

@app.delete("/chat/{conversation_id}")
async def clear_conversation(conversation_id: str):
    """清除指定对话历史"""
    if conversation_id in conversations:
        del conversations[conversation_id]
        return {"message": f"对话 {conversation_id} 已清除"}
    return {"message": "对话不存在"}

@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {"status": "healthy", "service": "ChatGPT API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)