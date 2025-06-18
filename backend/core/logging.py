#!/usr/bin/env python3
"""
日志配置模块

统一配置应用的日志系统。
"""

import logging
import sys
from typing import Optional
from .config import settings

def setup_logging(log_level: Optional[str] = None) -> logging.Logger:
    """
    设置应用日志配置
    
    Args:
        log_level: 日志级别，如果不提供则使用配置文件中的设置
    
    Returns:
        配置好的logger实例
    """
    level = log_level or settings.LOG_LEVEL
    
    # 配置日志格式
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # 配置根日志器
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # 创建应用专用的logger
    logger = logging.getLogger("agentarena")
    
    # 设置第三方库的日志级别
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("fastapi").setLevel(logging.INFO)
    
    return logger

# 创建全局logger实例
logger = setup_logging()