# AgentArena Makefile
# 一键运行前后端项目的便捷工具

.PHONY: help install install-backend install-frontend dev dev-backend dev-frontend build clean stop

# 默认目标
help:
	@echo "🚀 AgentArena 项目管理工具"
	@echo ""
	@echo "可用命令:"
	@echo "  make install        - 安装所有依赖 (前端+后端)"
	@echo "  make install-backend - 安装后端依赖"
	@echo "  make install-frontend - 安装前端依赖"
	@echo "  make dev            - 启动开发环境 (前端+后端)"
	@echo "  make dev-backend    - 仅启动后端服务"
	@echo "  make dev-frontend   - 仅启动前端服务"
	@echo "  make build          - 构建生产版本"
	@echo "  make clean          - 清理依赖和缓存"
	@echo "  make stop           - 停止所有服务"
	@echo "  make setup-env      - 创建环境变量文件"
	@echo ""

# 安装所有依赖
install: install-backend install-frontend
	@echo "✅ 所有依赖安装完成!"

# 安装后端依赖
install-backend:
	@echo "📦 安装后端依赖..."
	cd backend && pip install -r requirements.txt
	@echo "✅ 后端依赖安装完成!"

# 安装前端依赖
install-frontend:
	@echo "📦 安装前端依赖..."
	cd frontend && npm install
	@echo "✅ 前端依赖安装完成!"

# 创建环境变量文件
setup-env:
	@echo "🔧 设置环境变量..."
	@if [ ! -f backend/.env ]; then \
		cp backend/.env.example backend/.env 2>/dev/null || echo "OPENAI_API_KEY=your-api-key-here" > backend/.env; \
		echo "📝 请编辑 backend/.env 文件，添加你的 OPENAI_API_KEY"; \
	else \
		echo "✅ 环境变量文件已存在"; \
	fi

# 启动开发环境 (并行启动前后端)
dev: setup-env
	@echo "🚀 启动开发环境..."
	@echo "后端: http://localhost:8000"
	@echo "前端: http://localhost:3000"
	@echo "按 Ctrl+C 停止服务"
	@trap 'make stop' INT; \
	make dev-backend & \
	make dev-frontend & \
	wait

# 仅启动后端服务
dev-backend: setup-env
	@echo "🔧 启动后端服务..."
	@echo "后端API: http://localhost:8000"
	@echo "API文档: http://localhost:8000/docs"
	cd backend && python main.py

# 仅启动前端服务
dev-frontend:
	@echo "🎨 启动前端服务..."
	@echo "前端界面: http://localhost:3000"
	cd frontend && npm run dev

# 构建生产版本
build:
	@echo "🏗️ 构建生产版本..."
	cd frontend && npm run build
	@echo "✅ 前端构建完成! 输出目录: frontend/dist"

# 清理依赖和缓存
clean:
	@echo "🧹 清理项目..."
	@echo "清理前端依赖..."
	@rm -rf frontend/node_modules frontend/dist
	@echo "清理Python缓存..."
	@find backend -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	@find backend -name "*.pyc" -delete 2>/dev/null || true
	@echo "✅ 清理完成!"

# 停止所有服务
stop:
	@echo "🛑 停止所有服务..."
	@pkill -f "python main.py" 2>/dev/null || true
	@pkill -f "npm run dev" 2>/dev/null || true
	@pkill -f "vite" 2>/dev/null || true
	@echo "✅ 服务已停止!"

# 快速重启
restart: stop dev

# 检查项目状态
status:
	@echo "📊 项目状态检查..."
	@echo "后端依赖:"
	@cd backend && pip list | grep -E "fastapi|langchain|uvicorn" || echo "❌ 后端依赖未安装"
	@echo "前端依赖:"
	@cd frontend && npm list --depth=0 2>/dev/null | grep -E "vue|vite|axios" || echo "❌ 前端依赖未安装"
	@echo "环境变量:"
	@if [ -f backend/.env ]; then echo "✅ .env 文件存在"; else echo "❌ .env 文件不存在"; fi

# 运行测试
test:
	@echo "🧪 运行测试..."
	@echo "后端健康检查..."
	@curl -s http://localhost:8000/health > /dev/null && echo "✅ 后端服务正常" || echo "❌ 后端服务未启动"

# 显示日志
logs:
	@echo "📋 显示服务日志..."
	@echo "如果服务正在运行，日志将显示在终端中"

# 一键部署到生产环境
deploy: clean install build
	@echo "🚀 部署完成!"
	@echo "前端文件位于: frontend/dist"
	@echo "后端服务可通过: cd backend && python main.py 启动"