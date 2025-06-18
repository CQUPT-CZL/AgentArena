#!/usr/bin/env python3
"""
应用配置模块

集中管理所有的配置项，包括环境变量、API设置等。
"""

import os
from typing import List
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Settings:
    """应用设置类"""
    
    # 应用基本信息
    APP_NAME: str = "AgentArena API"
    APP_DESCRIPTION: str = "多Agent聊天API系统"
    VERSION: str = "1.0.0"
    
    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # CORS配置
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",  # Vite默认端口
    ]
    
    # OpenAI配置
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_API_BASE: str = os.getenv("OPENAI_API_BASE", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "deepseek-chat")
    
    # 日志配置
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Agent配置
    DEFAULT_AGENT: str = "simple_chat"
    MAX_CONVERSATION_HISTORY: int = 50
    
    def __init__(self):
        """初始化设置，验证必要的环境变量"""
        if not self.OPENAI_API_KEY:
            print("⚠️  警告: 未设置OPENAI_API_KEY环境变量，某些Agent可能无法正常工作")

# 创建全局设置实例
settings = Settings()