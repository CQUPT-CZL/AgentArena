import os
from typing import Dict, List
from datetime import datetime
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import AIMessage, HumanMessage
from dotenv import load_dotenv
from ..base import BaseAgent
from core.config import settings
from core.logging import logger

# 加载环境变量
load_dotenv()

class LangChainAgent(BaseAgent):
    """LangChain智能Agent - 具备工具调用能力"""
    
    def __init__(self):
        super().__init__(
            name="langchain_agent",
            display_name="智能助手",
            description="具备工具调用能力的智能助手，可以获取时间、进行计算、查询天气等",
            version="1.0.0"
        )
        
        # 初始化聊天模型
        api_key = settings.OPENAI_API_KEY
        if not api_key:
            logger.warning("未设置OPENAI_API_KEY，LangChainAgent可能无法正常工作")
            self.llm = None
            self.agent_executor = None
        else:
            self.llm = ChatOpenAI(
                model=settings.OPENAI_MODEL,
                api_key=api_key,
                temperature=0.7
            )
            
            # 创建工具和agent
            self.tools = self._create_tools()
            self.agent_executor = self._create_agent()
        
    def _create_tools(self) -> List:
        """创建工具列表"""
        
        @tool
        def get_current_time(query: str = "") -> str:
            """获取当前时间"""
            now = datetime.now()
            return f"当前时间是：{now.strftime('%Y年%m月%d日 %H:%M:%S')}"
        
        @tool
        def calculate(expression: str) -> str:
            """进行数学计算，输入数学表达式"""
            try:
                # 只允许基本的数学运算
                allowed_chars = set('0123456789+-*/().= ')
                if not all(c in allowed_chars for c in expression):
                    return "错误：只支持基本数学运算符"
                
                result = eval(expression)
                return f"计算结果：{expression} = {result}"
            except Exception as e:
                return f"计算错误：{str(e)}"
        
        @tool
        def search_weather(city: str) -> str:
            """查询天气信息，输入城市名称"""
            # 这里是模拟的天气查询，实际项目中可以接入真实的天气API
            weather_data = {
                "北京": "晴天，温度15-25°C",
                "上海": "多云，温度18-28°C",
                "广州": "小雨，温度20-30°C",
                "深圳": "晴天，温度22-32°C"
            }
            
            return weather_data.get(city, f"抱歉，暂时无法获取{city}的天气信息")
        
        return [get_current_time, calculate, search_weather]
    
    def _create_agent(self):
        """创建LangChain agent"""
        prompt = ChatPromptTemplate.from_messages([
            ("system", "你是一个智能助手，可以使用工具来帮助用户。请根据用户的问题选择合适的工具。"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ])
        
        agent = create_openai_tools_agent(self.llm, self.tools, prompt)
        return AgentExecutor(agent=agent, tools=self.tools, verbose=True)
    

    
    async def process_message(self, message: str, conversation_id: str = "default") -> str:
        """处理用户消息"""
        try:
            if not self.agent_executor:
                return "抱歉，LangChain Agent未配置，无法处理您的消息。请检查OPENAI_API_KEY环境变量。"
            
            # 添加用户消息到历史
            self.add_to_conversation(conversation_id, "user", message)
            
            # 使用agent处理消息
            response = await self.agent_executor.ainvoke({
                "input": message,
                "chat_history": self._format_chat_history(conversation_id)
            })
            
            ai_response = response["output"]
            
            # 添加AI回复到历史
            self.add_to_conversation(conversation_id, "assistant", ai_response)
            
            logger.info(f"LangChainAgent处理消息: {message[:50]}... -> {ai_response[:50]}...")
            
            return ai_response
            
        except Exception as e:
            error_msg = f"抱歉，处理您的消息时出现错误: {str(e)}"
            logger.error(f"LangChainAgent错误: {str(e)}")
            return error_msg
    
    def _format_chat_history(self, conversation_id: str) -> List:
        """格式化聊天历史为LangChain格式"""
        history = []
        conversation_history = self.get_conversation_history(conversation_id)
        for msg in conversation_history:
            if msg["role"] == "user":
                history.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                history.append(AIMessage(content=msg["content"]))
        return history
    
    def get_capabilities(self) -> List[str]:
        """获取Agent能力列表"""
        return [
            "智能对话",
            "工具调用",
            "时间查询",
            "数学计算",
            "天气查询",
            "多轮对话"
        ]