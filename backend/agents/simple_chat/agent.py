import os
from pyexpat import model
import re
from typing import List
# from openai import ChatOpenAIs
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from ..base import BaseAgent
from core.config import settings
from core.logging import logger

# 加载环境变量
load_dotenv()

class SimpleChatAgent(BaseAgent):
    """简单聊天Agent - 基础的ChatGPT对话功能"""
    
    def __init__(self):
        super().__init__(
            name="simple_chat",
            display_name="简单对话",
            description="基础的ChatGPT对话功能，适合日常聊天和简单问答",
            version="1.0.0"
        )
        
        # 初始化OpenAI客户端
        api_key = settings.OPENAI_API_KEY
        api_base = settings.OPENAI_API_BASE
        model_name = settings.OPENAI_MODEL
        if not api_key:
            logger.warning("未设置OPENAI_API_KEY，SimpleChatAgent可能无法正常工作")
            self.client = None
        else:
            self.client = ChatOpenAI(api_key=api_key, base_url=api_base, model=model_name)
        
        self.model = settings.OPENAI_MODEL
        

    
    async def process_message(self, message: str, conversation_id: str = "default") -> str:
        """处理用户消息"""
        try:
            if not self.client:
                return "抱歉，OpenAI API未配置，无法处理您的消息。请检查OPENAI_API_KEY环境变量。"
            
            # 添加用户消息到历史
            self.add_to_conversation(conversation_id, "user", message)
            
            # 获取对话历史（转换为OpenAI格式）
            history = self.get_conversation_history(conversation_id)
            openai_messages = [
                {"role": msg["role"], "content": msg["content"]}
                for msg in history
            ]
            
            # 调用OpenAI API
            # response = await self.client.ainvoke(
            #     input={
            #         "messages": openai_messages,
            #     }
            # )

            response = await self.client.ainvoke(openai_messages)

            print(response)
            
            # ai_response = response.choices[0].message.content
            ai_response = response.content
            
            # 添加AI回复到历史
            self.add_to_conversation(conversation_id, "assistant", ai_response)
            
            logger.info(f"SimpleChatAgent处理消息: {message[:50]}... -> {ai_response[:50]}...")
            
            return ai_response
            
        except Exception as e:
            error_msg = f"抱歉，处理您的消息时出现错误: {str(e)}"
            logger.error(f"SimpleChatAgent错误: {str(e)}")
            return error_msg
    
    def get_capabilities(self) -> List[str]:
        """获取Agent能力列表"""
        return [
            "基础对话",
            "问答回复",
            "文本生成",
            "多轮对话"
        ]