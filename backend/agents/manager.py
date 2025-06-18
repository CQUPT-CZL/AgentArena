from typing import Dict, List, Optional, Any
from core.logging import logger
from core.config import settings
from .simple_chat import SimpleChatAgent
from .langchain_agent import LangChainAgent

class AgentManager:
    """Agent管理器"""
    
    def __init__(self):
        self.agents: Dict[str, Any] = {}
        self._initialize_agents()
    
    def _initialize_agents(self):
        """初始化所有agent"""
        try:
            # 注册简单聊天agent
            simple_agent = SimpleChatAgent()
            self.agents[simple_agent.name] = simple_agent
            
            # 注册LangChain agent
            langchain_agent = LangChainAgent()
            self.agents[langchain_agent.name] = langchain_agent
            
            logger.info(f"已注册 {len(self.agents)} 个agent: {list(self.agents.keys())}")
            
        except Exception as e:
            logger.error(f"初始化agent失败: {str(e)}")
            raise
    
    def get_agent(self, agent_name: str) -> Optional[Any]:
        """获取指定的agent"""
        return self.agents.get(agent_name)
    
    def get_available_agents(self) -> List[Dict[str, str]]:
        """获取所有可用的agent信息"""
        agent_list = []
        for agent_name, agent in self.agents.items():
            agent_info = {
                "name": agent.name,
                "display_name": agent.display_name,
                "description": agent.description
            }
            agent_list.append(agent_info)
        return agent_list
    
    async def process_message(self, agent_name: str, message: str, conversation_id: str = "default") -> str:
        """使用指定agent处理消息"""
        agent = self.get_agent(agent_name)
        if not agent:
            raise ValueError(f"Agent '{agent_name}' 不存在")
        
        return await agent.process_message(message, conversation_id)
    
    def clear_conversation(self, agent_name: str, conversation_id: str) -> bool:
        """清除指定agent的对话历史"""
        agent = self.get_agent(agent_name)
        if not agent:
            return False
        
        return agent.clear_conversation(conversation_id)
    
    def get_agent_stats(self) -> Dict[str, Any]:
        """获取所有agent的统计信息"""
        stats = {}
        for agent_name, agent in self.agents.items():
            stats[agent_name] = {
                "name": agent.name,
                "display_name": agent.display_name,
                "conversation_count": agent.get_conversation_count()
            }
        return stats

# 全局agent管理器实例
agent_manager = AgentManager()