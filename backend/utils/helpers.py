#!/usr/bin/env python3
"""
工具函数模块

提供各种通用的辅助函数。
"""

import re
from datetime import datetime
from typing import Optional

def format_timestamp(dt: Optional[datetime] = None) -> str:
    """
    格式化时间戳
    
    Args:
        dt: 要格式化的datetime对象，如果为None则使用当前时间
    
    Returns:
        格式化后的时间字符串
    """
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def validate_agent_name(agent_name: str) -> bool:
    """
    验证Agent名称是否有效
    
    Args:
        agent_name: 要验证的Agent名称
    
    Returns:
        是否有效
    """
    # Agent名称应该只包含字母、数字和下划线
    pattern = r'^[a-zA-Z][a-zA-Z0-9_]*$'
    return bool(re.match(pattern, agent_name))

def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    截断文本
    
    Args:
        text: 要截断的文本
        max_length: 最大长度
        suffix: 截断后的后缀
    
    Returns:
        截断后的文本
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix

def sanitize_conversation_id(conversation_id: str) -> str:
    """
    清理对话ID，确保安全
    
    Args:
        conversation_id: 原始对话ID
    
    Returns:
        清理后的对话ID
    """
    # 移除特殊字符，只保留字母、数字、下划线和连字符
    sanitized = re.sub(r'[^a-zA-Z0-9_-]', '', conversation_id)
    return sanitized or "default"