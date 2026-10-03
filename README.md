# Toutiao Demo — 类头条资讯后端 API

基于 **FastAPI + SQLAlchemy 2.0 (async) + MySQL** 实现的资讯类后端服务，配套 Vue3 + Vant 前端联调。

## 技术栈

- Web 框架：FastAPI 0.125
- ORM：SQLAlchemy 2.0（异步）+ aiomysql
- 数据库：MySQL 8.x
- 数据校验：Pydantic v1
- 鉴权：JWT（python-jose）+ passlib/bcrypt 密码哈希
- 服务器：Uvicorn

## 项目结构

```
TouTiao Demo/
├── main.py              # 入口，注册路由、中间件、异常处理
├── config/
│   └── db_config.py     # 异步引擎、连接池、get_db 依赖
├── models/              # SQLAlchemy ORM 模型
│   ├── user.py          # 用户表 + 用户令牌表
│   └── news.py          # 新闻表 + 分类表
├── schemas/             # Pydantic 请求/响应模型
│   └── user.py
├── crud/                # 数据库操作封装
│   ├── user.py
│   └── news.py
├── routers/             # 路由层
│   ├── user.py          # /api/user/*
│   └── news.py          # /api/news/*
└── utils/
    ├── auth.py          # get_current_user 依赖
    ├── response.py      # 统一响应体
    └── password_security.py
```

## 主要接口

### 用户模块 `/api/user`

| 方法 | 路径 | 说明 |
|---|---|---|
| POST | `/register` | 注册 |
| POST | `/login` | 登录，返回 JWT |
| GET  | `/info` | 获取当前用户信息（需登录） |
| PUT  | `/update` | 修改昵称/头像/性别/简介/手机号 |
| PUT  | `/password` | 修改密码（需校验旧密码） |

### 新闻模块 `/api/news`

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/categories` | 新闻分类列表 |
| GET | `/list?categoryId=&page=&pageSize=` | 分页新闻列表 |
| GET | `/detail?id=` | 新闻详情，自动自增浏览量并返回相关推荐 |

## 本地启动

```bash
# 1. 创建虚拟环境并安装依赖
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/Mac
pip install -r requirements.txt

# 2. 建库（MySQL 中执行）
CREATE DATABASE news_app DEFAULT CHARSET utf8mb4;

# 3. 修改 config/db_config.py 里的数据库连接地址
#    mysql+aiomysql://用户名:密码@localhost:3306/news_app

# 4. 启动
uvicorn main:app --reload
```

启动后访问 `http://localhost:8000/docs` 查看 Swagger 接口文档。

## 实现要点

- **分层架构**：routers（路由）/ crud（数据操作）/ models（ORM）/ schemas（数据校验）解耦
- **异步数据库会话**：通过 FastAPI 依赖注入统一管理 commit / rollback / close，配置连接池 pool_size=10
- **索引优化**：对新闻表高频查询字段 `category_id`、`publish_time` 建联合索引
- **统一响应体**：所有接口返回 `{code, message, data}` 结构，统一异常处理
- **鉴权**：登录签发 JWT，通过 `Depends(get_current_user)` 在需要登录的接口自动校验
