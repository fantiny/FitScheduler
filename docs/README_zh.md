# FitScheduler

预约系统后端 API 服务，用于体育教练和场地预订管理。

## 项目概述

FitScheduler 是一个全功能的预约管理系统，专为体育教练和场地预约设计。系统支持：

- 用户、教练和场地管理
- 预约创建和管理
- 支付方式管理
- 评价和收藏功能
- 身份验证和授权
- 不同用户角色的权限控制

## 安装指南

### 环境要求

- Python 3.8+
- MySQL 5.7+
- Node.js 16+ (前端部分)

### 安装步骤

1. 克隆代码仓库：

```bash
git clone https://github.com/yourusername/bsweetOrder-yoyaku.git
cd bsweetOrder-yoyaku
```

2. 创建虚拟环境并激活：

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. 安装依赖：

```bash
# 生产环境依赖
pip install -r requirements.txt --prefer-binary

# 开发环境依赖 (包含测试工具和代码质量工具)
pip install -r requirements-dev.txt --prefer-binary
```

> **注意**: 使用`--prefer-binary`选项可以优先安装预编译的二进制包，避免需要Rust编译工具链的问题。如果仍然遇到与Rust相关的错误，请确保已安装[Rust工具链](https://www.rust-lang.org/tools/install)。

4. 配置环境变量（或创建 .env 文件）：

```
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_user
DB_PASSWORD=your_password
DB_NAME=yoyaku
SECRET_KEY=your_secret_key
```

5. 初始化数据库：

```bash
python app/db/init_db.py
```

6. 启动应用：

#### 使用启动脚本 (推荐)

在Windows系统下，可以直接双击以下批处理文件启动服务：

- `start-app.bat` - 启动后端API服务

启动脚本会自动检查环境、创建虚拟环境、安装依赖并启动服务。

#### 手动启动

```bash
uvicorn main:app --reload --port 8000
```

服务将在 http://localhost:8000 启动，API 文档可在 http://localhost:8000/docs 访问。

## 项目结构

```
yoyaku/
├── app/                      # 应用程序核心代码
│   ├── api/                  # API层
│   │   ├── dependencies/     # 共享依赖项 (auth, permissions)
│   │   └── v1/               # API版本1
│   │       ├── endpoints/    # 各个资源端点
│   │       └── router.py     # 主路由配置
│   │
│   ├── core/                 # 核心配置
│   │   ├── config.py         # 配置文件
│   │   ├── security.py       # 安全相关
│   │   └── environment.py    # 环境配置
│   │
│   ├── db/                   # 数据库相关
│   │   ├── base.py           # Base模型类
│   │   ├── session.py        # 数据库会话
│   │   └── init_db.py        # 数据库初始化
│   │
│   ├── models/               # 数据库模型(ORM)
│   │
│   ├── schemas/              # Pydantic模型(请求/响应)
│   │
│   ├── services/             # 业务逻辑层
│   │
│   └── utils/                # 通用工具函数
│
├── alembic/                  # 数据库迁移
│   └── versions/             # 迁移版本
│
├── sql/                      # SQL脚本
│   └── ddl.sql               # 数据库定义
│
├── tests/                    # 测试代码
│   ├── unit_test.py          # 单元测试
│   ├── integration_test.py   # 集成测试
│   ├── test_setup.py         # 测试数据设置
│   └── testing_guide.md      # 测试指南
│
├── docs/                     # 文档
│   ├── README_zh.md          # 中文文档（当前）
│   └── README_ja.md          # 日语文档
│
├── .env                      # 环境变量
│
├── .env.example              # 环境变量示例
│
├── .gitignore                # Git忽略文件
│
├── .dockerignore             # Docker忽略文件
│
├── alembic.ini               # Alembic配置
│
├── main.py                   # 应用入口点
│
├── requirements.txt          # 生产环境依赖
│
├── requirements-dev.txt      # 开发环境依赖
│
└── start-app.bat             # 后端服务启动脚本
```

## 前端项目

本项目具有单独的前端仓库 `fitscheduler-frontend`，它使用Vue 3和Vite构建。前端项目通过API与本后端项目进行通信。

前端项目仓库: [FitScheduler Frontend](../../fitscheduler-frontend)

### 启动前端项目

前端项目可以通过以下方式启动：

1. 使用启动脚本（在前端项目目录中）：
   - `start-frontend.bat` - 启动前端开发服务器

2. 手动启动：
```bash
cd ../fitscheduler-frontend
npm install
npm run dev
```

前端服务将在 http://localhost:5173 启动。

## API 使用指南

### 认证

API 使用 JWT 令牌进行认证。获取令牌的步骤：

1. 注册新用户：

```
POST /api/v1/auth/register
{
  "email": "user@example.com",
  "username": "example_user",
  "password": "secure_password",
  "phone": "12345678901"
}
```

2. 登录并获取令牌：

```
POST /api/v1/auth/login
{
  "username": "user@example.com",
  "password": "secure_password"
}
```

3. 使用令牌进行后续请求：

```
Authorization: Bearer <your_token>
```

### 主要 API 端点

- `/api/v1/auth/*` - 认证相关
- `/api/v1/users/*` - 用户管理
- `/api/v1/coaches/*` - 教练管理
- `/api/v1/venues/*` - 场地管理
- `/api/v1/bookings/*` - 预约管理
- `/api/v1/reviews/*` - 评价管理
- `/api/v1/lesson-types/*` - 课程类型管理

完整 API 文档可在运行应用后访问 `/docs` 端点。

## 开发指南

### 代码风格

项目遵循 PEP8 编码规范，使用 FastAPI 官方推荐的项目结构。推荐使用以下工具进行代码质量控制：

- `black` - 自动格式化代码
- `flake8` - 代码风格检查

这些工具已包含在 `requirements-dev.txt` 中。

### 添加新特性

1. **创建新的数据库模型**：在 `app/models/` 目录下创建

2. **定义 Pydantic 模式**：在 `app/schemas/` 目录下创建请求和响应模式

3. **实现服务逻辑**：在 `app/services/` 目录下添加业务逻辑

4. **创建 API 端点**：在 `app/api/v1/endpoints/` 目录下添加新的路由

### 运行测试

首先确保已安装开发环境依赖：

```bash
pip install -r requirements-dev.txt
```

然后使用以下命令运行测试：

```bash
python tests/test_setup.py  # 创建测试数据
pytest tests/unit_test.py   # 运行单元测试
pytest tests/integration_test.py  # 运行集成测试
```

### 数据库迁移

使用 Alembic 进行数据库迁移：

```bash
# 创建迁移脚本
alembic revision --autogenerate -m "描述变更"

# 应用迁移
alembic upgrade head
```

## 贡献指南

欢迎提交 Pull Request 和报告 Issues。请确保代码通过所有测试并遵循项目编码规范。

## 许可证

本项目采用 MIT 许可证。

## 语言

本文档有多种语言版本：
- [English](../README.md)
- [中文](README_zh.md) (当前)
- [日本語](README_ja.md) 