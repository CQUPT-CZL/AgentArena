#!/usr/bin/env python3
"""
聊天相关的数据模型

定义聊天消息和响应的数据结构。
"""

from pydantic import BaseModel, Field
from typing import Optional
from core.config import settings

class ChatMessage(BaseModel):
    """聊天消息模型"""
    message: str = Field(..., description="用户发送的消息内容", min_length=1)
    agent_name: str = Field(
        default=settings.DEFAULT_AGENT,
        description="要使用的Agent名称"
    )
    conversation_id: str = Field(
        default="default",
        description="对话ID，用于区分不同的对话会话"
    )

class ChatResponse(BaseModel):
    """聊天响应模型"""
    response: str = Field(..., description="Agent的回复内容")
    agent_name: str = Field(..., description="处理消息的Agent名称")
    conversation_id: str = Field(..., description="对话ID")
    timestamp: Optional[str] = Field(None, description="响应时间戳")