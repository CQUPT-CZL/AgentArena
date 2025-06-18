#!/usr/bin/env python3
"""
AgentArena 后端服务启动文件

这是整个后端应用的入口点，负责启动FastAPI服务器。
"""

import uvicorn
from api.main import app

if __name__ == "__main__":
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )