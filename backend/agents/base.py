#!/usr/bin/env python3
"""
Agent基础类

定义所有Agent必须实现的接口和通用功能。
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime
from core.logging import logger
from utils.helpers import format_timestamp

class BaseAgent(ABC):
    """Agent基础抽象类"""
    
    def __init__(self, name: str, display_name: str, description: str, version: str = "1.0.0"):
        """
        初始化Agent
        
        Args:
            name: Agent的唯一标识名称
            display_name: Agent的显示名称
            description: Agent的功能描述
            version: Agent版本
        """
        self.name = name
        self.display_name = display_name
        self.description = description
        self.version = version
        self.conversations: Dict[str, List[Dict[str, Any]]] = {}
        self.created_at = datetime.now()
        self.last_activity = None
        
        logger.info(f"初始化Agent: {self.display_name} ({self.name})")
    
    @abstractmethod
    async def process_message(self, message: str, conversation_id: str = "default") -> str:
        """
        处理用户消息（抽象方法，子类必须实现）
        
        Args:
            message: 用户消息
            conversation_id: 对话ID
        
        Returns:
            Agent的回复
        """
        pass
    
    def add_to_conversation(self, conversation_id: str, role: str, content: str) -> None:
        """
        添加消息到对话历史
        
        Args:
            conversation_id: 对话ID
            role: 角色（user/assistant）
            content: 消息内容
        """
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []
        
        self.conversations[conversation_id].append({
            "role": role,
            "content": content,
            "timestamp": format_timestamp()
        })
        
        self.last_activity = datetime.now()
        
        # 限制对话历史长度
        max_history = 50
        if len(self.conversations[conversation_id]) > max_history:
            self.conversations[conversation_id] = self.conversations[conversation_id][-max_history:]
    
    def get_conversation_history(self, conversation_id: str) -> List[Dict[str, Any]]:
        """
        获取对话历史
        
        Args:
            conversation_id: 对话ID
        
        Returns:
            对话历史列表
        """
        return self.conversations.get(conversation_id, [])
    
    def clear_conversation(self, conversation_id: str) -> bool:
        """
        清除对话历史
        
        Args:
            conversation_id: 对话ID
        
        Returns:
            是否成功清除
        """
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
            logger.info(f"Agent {self.name} 清除对话 {conversation_id}")
            return True
        return False
    
    def get_conversation_count(self) -> int:
        """
        获取对话数量
        
        Returns:
            对话数量
        """
        return len(self.conversations)
    
    def get_total_messages(self) -> int:
        """
        获取总消息数
        
        Returns:
            总消息数
        """
        total = 0
        for conversation in self.conversations.values():
            total += len(conversation)
        return total
    
    def get_agent_info(self) -> Dict[str, Any]:
        """
        获取Agent信息
        
        Returns:
            Agent信息字典
        """
        return {
            "name": self.name,
            "display_name": self.display_name,
            "description": self.description,
            "version": self.version,
            "capabilities": self.get_capabilities(),
            "conversation_count": self.get_conversation_count(),
            "total_messages": self.get_total_messages(),
            "created_at": format_timestamp(self.created_at),
            "last_activity": format_timestamp(self.last_activity) if self.last_activity else None
        }
    
    def get_capabilities(self) -> List[str]:
        """
        获取Agent能力列表（子类可以重写）
        
        Returns:
            能力列表
        """
        return ["基础对话"]
    
    def __str__(self) -> str:
        return f"{self.display_name} ({self.name})"
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.name}>"