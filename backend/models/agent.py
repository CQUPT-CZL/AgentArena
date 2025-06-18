#!/usr/bin/env python3
"""
Agent相关的数据模型

定义Agent信息和统计数据的结构。
"""

from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

class AgentInfo(BaseModel):
    """Agent信息模型"""
    name: str = Field(..., description="Agent的唯一标识名称")
    display_name: str = Field(..., description="Agent的显示名称")
    description: str = Field(..., description="Agent的功能描述")
    version: Optional[str] = Field(None, description="Agent版本")
    capabilities: Optional[list] = Field(None, description="Agent的能力列表")

class AgentStats(BaseModel):
    """Agent统计信息模型"""
    agent_name: str = Field(..., description="Agent名称")
    conversation_count: int = Field(..., description="对话数量")
    total_messages: int = Field(default=0, description="总消息数")
    last_activity: Optional[str] = Field(None, description="最后活动时间")
    
class AgentStatus(BaseModel):
    """Agent状态模型"""
    name: str = Field(..., description="Agent名称")
    status: str = Field(..., description="Agent状态: active, inactive, error")
    uptime: Optional[str] = Field(None, description="运行时间")
    error_message: Optional[str] = Field(None, description="错误信息")