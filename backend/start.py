#!/usr/bin/env python3
"""
启动脚本 - 使用 uv 运行 FastAPI 应用
"""

import subprocess
import sys

def main():
    """启动 FastAPI 应用"""
    try:
        # 使用 uv run 启动 uvicorn
        cmd = [
            "uv", "run", "uvicorn", "main:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload"
        ]
        
        print("🚀 启动 AgentArena Backend API...")
        print(f"📝 命令: {' '.join(cmd)}")
        print("🌐 服务地址: http://localhost:8000")
        print("📚 API 文档: http://localhost:8000/docs")
        print("\n按 Ctrl+C 停止服务\n")
        
        subprocess.run(cmd, check=True)
        
    except KeyboardInterrupt:
        print("\n👋 服务已停止")
    except subprocess.CalledProcessError as e:
        print(f"❌ 启动失败: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("❌ 错误: 未找到 uv 命令，请先安装 uv")
        print("💡 安装命令: curl -LsSf https://astral.sh/uv/install.sh | sh")
        sys.exit(1)

if __name__ == "__main__":
    main()