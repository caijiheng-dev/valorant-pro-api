# Valorant Pro Player API — 无畏契约职业选手信息后端

基于 **FastAPI + SQLAlchemy 2.0 (async) + MySQL** 的无畏契约职业选手信息查询后端，提供战队、选手列表、选手详情（含准星代码、灵敏度、生涯成就）接口。

## 技术栈

- Web 框架：FastAPI
- ORM：SQLAlchemy 2.0（异步）+ aiomysql
- 数据库：MySQL 8.x
- 数据校验：Pydantic v1
- 鉴权：JWT（python-jose）+ passlib/bcrypt 密码哈希

## 项目结构

```
TouTiao Demo/
├── main.py              # 入口
├── config/
│   └── db_config.py     # 异步引擎、连接池、get_db 依赖
├── models/
│   ├── user.py          # 用户表
│   └── player.py        # 战队表 + 选手表
├── schemas/
│   └── user.py
├── crud/
│   ├── user.py
│   └── player.py
├── routers/
│   ├── user.py          # /api/user/*
│   └── player.py        # /api/players/*
├── utils/
└── seed_players.sql     # 种子数据（建表 + 10 名职业选手）
```

## 主要接口

### 选手模块 `/api/players`

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/teams` | 战队列表 |
| GET | `/list?teamId=&page=&pageSize=` | 选手分页列表 |
| GET | `/detail?id=` | 选手详情（准星代码、灵敏度、生涯成就、同战队推荐） |

### 用户模块 `/api/user`

| 方法 | 路径 | 说明 |
|---|---|---|
| POST | `/register` | 注册 |
| POST | `/login` | 登录，返回 token |
| GET  | `/info` | 获取当前用户信息（需登录） |
| PUT  | `/update` | 修改个人资料 |
| PUT  | `/password` | 修改密码 |

## 本地启动

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# 建库并导入种子数据
mysql -u root -p -e "CREATE DATABASE news_app DEFAULT CHARSET utf8mb4;"
mysql -u root -p news_app < seed_players.sql

# 修改 config/db_config.py 里的数据库连接
uvicorn main:app --reload
```

访问 `http://localhost:8000/docs` 查看 Swagger 文档。

## 已收录选手（示例）

| 战队 | 选手 | 位置 | 亮点 |
|---|---|---|---|
| EDward Gaming | ZmjjKK | 决斗 | 2024 Champions 冠军 + MVP |
| EDward Gaming | CHICHOO | 哨位 | 2024 Champions 冠军 |
| Sentinels | TenZ | 决斗 | 2021 Masters Reykjavík 冠军 |
| LOUD | aspas | 决斗 | 2022 Champions 冠军 |

选手的 DPI、游戏内灵敏度、准星代码均可直接在游戏内导入使用。
