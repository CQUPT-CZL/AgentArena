# 🚀 UV 项目管理指南

本项目已迁移到使用 `uv` 进行 Python 包管理，这是一个超快速的 Python 包管理器和项目管理工具。

## 📦 什么是 uv？

`uv` 是由 Astral 公司开发的现代 Python 包管理器，具有以下优势：

- ⚡ **极快的安装速度**：比 `pip` 快 10-100 倍
- 🔒 **可靠的依赖解析**：避免版本冲突
- 🛠️ **项目管理**：类似于 `poetry` 的功能
- 🔄 **兼容性**：与现有的 `pip` 和 `requirements.txt` 兼容

## 🛠️ 安装 uv

### macOS/Linux
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Windows
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 使用 pip
```bash
pip install uv
```

## 🚀 项目使用指南

### 1. 安装项目依赖

```bash
cd backend
uv sync
```

### 2. 启动开发服务器

#### 方式一：使用 uv run
```bash
cd backend
uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

#### 方式二：使用启动脚本
```bash
cd backend
python start.py
```

### 3. 添加新依赖

```bash
cd backend
# 添加运行时依赖
uv add requests

# 添加开发依赖
uv add --dev pytest

# 添加特定版本
uv add "fastapi>=0.100.0"
```

### 4. 移除依赖

```bash
cd backend
uv remove package-name
```

### 5. 更新依赖

```bash
cd backend
# 更新所有依赖
uv sync --upgrade

# 更新特定依赖
uv add package-name --upgrade
```

### 6. 查看依赖树

```bash
cd backend
uv tree
```

## 📁 项目结构

```
backend/
├── pyproject.toml    # 项目配置和依赖声明
├── uv.lock          # 锁定的依赖版本（类似 package-lock.json）
├── .python-version  # Python 版本声明
├── start.py         # 启动脚本
├── main.py          # FastAPI 应用
├── requirements.txt # 传统依赖文件（保留用于兼容）
└── README.md        # 项目说明
```

## 🔧 配置文件说明

### pyproject.toml

这是项目的主要配置文件，包含：

- **项目元数据**：名称、版本、描述等
- **依赖声明**：运行时和开发依赖
- **构建配置**：打包和分发设置
- **工具配置**：代码格式化、linting 等

### uv.lock

这是依赖锁定文件，包含：

- **精确的版本号**：确保环境一致性
- **依赖树**：完整的依赖关系
- **哈希值**：确保包的完整性

> ⚠️ **重要**：`uv.lock` 文件应该提交到版本控制系统中！

## 🆚 uv vs 传统工具对比

| 功能 | pip + venv | poetry | uv |
|------|------------|--------|----||
| 安装速度 | 慢 | 中等 | 极快 |
| 依赖解析 | 基础 | 好 | 优秀 |
| 项目管理 | 手动 | 自动 | 自动 |
| 锁定文件 | 无 | poetry.lock | uv.lock |
| 虚拟环境 | 手动管理 | 自动 | 自动 |
| 配置文件 | requirements.txt | pyproject.toml | pyproject.toml |

## 🔄 从传统工具迁移

### 从 requirements.txt 迁移

```bash
# 1. 初始化 uv 项目
uv init

# 2. 从 requirements.txt 添加依赖
uv add -r requirements.txt

# 3. 删除旧文件（可选）
rm requirements.txt
```

### 从 poetry 迁移

```bash
# 1. 转换 pyproject.toml
# uv 可以直接读取 poetry 格式的 pyproject.toml

# 2. 同步依赖
uv sync

# 3. 更新锁定文件
rm poetry.lock
uv lock
```

## 🐛 常见问题

### Q: uv 和 conda 冲突吗？

A: 不冲突。uv 主要管理 Python 包，conda 管理 Python 环境。你可以在 conda 环境中使用 uv。

### Q: 如何在 CI/CD 中使用？

A: 
```yaml
# GitHub Actions 示例
- name: Install uv
  run: curl -LsSf https://astral.sh/uv/install.sh | sh

- name: Install dependencies
  run: uv sync

- name: Run tests
  run: uv run pytest
```

### Q: 如何设置私有包源？

A:
```bash
# 设置额外的包源
uv add --index-url https://pypi.org/simple/ --extra-index-url https://private.pypi.org/simple/ package-name
```

## 📚 更多资源

- [uv 官方文档](https://docs.astral.sh/uv/)
- [uv GitHub 仓库](https://github.com/astral-sh/uv)
- [Python 包管理最佳实践](https://packaging.python.org/)

## 🎯 下一步

1. 熟悉 `uv` 基本命令
2. 尝试添加/移除依赖
3. 体验快速的安装速度
4. 在团队中推广使用

---

💡 **提示**：如果遇到问题，可以随时回退到传统的 `pip` + `requirements.txt` 方式，两者可以并存使用。