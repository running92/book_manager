# 图书管理系统 Library Management System

一个面向毕业设计答辩展示的前后端分离 SPA 图书管理系统。开发环境前端和后端独立启动，生产/演示环境可由 Flask 直接托管 Vue 打包产物。

## 技术栈

- 前端：Vue 3、Vite、Element Plus、Pinia、Vue Router、vue-i18n、Axios、ECharts
- 后端：Python、Flask、Flask-SQLAlchemy、Flask-JWT-Extended、SQLite
- 部署：Vue Hash 路由 SPA，Flask 托管 `frontend/dist`

## 功能模块

- 登录认证：JWT 登录、刷新保持登录、退出登录、修改密码
- 权限控制：管理员和普通读者，前端路由/按钮控制，后端接口校验
- 仪表盘：统计卡片、最近借阅、分类分布、借阅趋势、读者提醒
- 图书管理：搜索、分类筛选、分页、新增、编辑、删除/下架、详情、封面上传
- 分类管理：新增、编辑、删除，分类下有图书时阻止删除
- 用户管理：新增、编辑、禁用、删除、重置密码
- 借阅管理：借书、还书、逾期状态、全部记录和我的记录
- 国际化：中文 / English 双语即时切换

## 目录结构

```text
book_manager/
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── extensions.py
│   ├── init_db.py
│   ├── requirements.txt
│   ├── uploads/
│   └── app/
│       ├── __init__.py
│       ├── models/
│       ├── routes/
│       ├── services/
│       └── utils/
└── frontend/
    ├── index.html
    ├── package.json
    ├── vite.config.js
    └── src/
        ├── api/
        ├── assets/
        ├── components/
        ├── layout/
        ├── locales/
        ├── router/
        ├── store/
        ├── utils/
        └── views/
```

## 默认账号

- 管理员：`admin` / `admin123`
- 普通读者：`user1` / `123456`

## 开发环境启动

后端：

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python init_db.py
python app.py
```

前端：

```bash
cd frontend
npm install
npm run dev
```

访问：`http://localhost:5173`。Vite 已配置 `/api` 和 `/uploads` 代理到 `http://localhost:5000`。

## 打包与演示部署

```bash
cd frontend
npm run build
cd ../backend
python app.py
```

访问：`http://localhost:5000`。如果端口被占用，可使用 `PORT=5001 python app.py` 并访问 `http://localhost:5001`。Flask 会托管 `frontend/dist`，非 `/api/*` 请求会回退到前端 `index.html`。

## SPA 路由说明

前端使用 `createWebHashHistory`，路由形式为 `/#/login`、`/#/dashboard`、`/#/books`。Hash 路由适合本地演示，刷新页面不易出现 404。

## 数据初始化

`python backend/init_db.py` 会重建 SQLite 数据库并写入演示数据：管理员、读者、6 个分类、10 本中英文图书和借阅记录。首次启动 Flask 时，如果数据库为空，也会自动创建表并插入演示数据。
