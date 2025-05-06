# 美家公寓智能服务平台

![项目封面图](可选图片URL)

## 项目概述

一个面向公寓管理的全栈 Web 应用，提供顾客端和业务管理端双重视角解决方案。采用前后端分离架构，实现客房展示、在线预订、用户管理等功能模块，已投入实际使用。

---

## 技术栈

### 前端技术

- **核心框架**: Vue3 + Composition API
- **UI 组件库**: Element-Plus
- **状态管理**: Pinia
- **路由管理**: Vue-Router
- **构建工具**: Vite
- **HTTP 客户端**: Axios（封装请求拦截/双 Token 无感刷新）
- **辅助工具**: TypeScript + ESLint

### 后端技术

- **服务框架**: Django REST Framework
- **数据库**: MySQL（ORM 操作）+ Redis 缓存
- **API 设计**: RESTful 规范 + GraphQL 混合模式

### 部署方案

- **容器化**: Docker + Docker-Compose
- **Web 服务器**: Nginx 反向代理
- **版本控制**: Git + GitHub Actions CI/CD

---

## 核心功能

| 模块     | 功能点               | 技术实现亮点              |
| -------- | -------------------- | ------------------------- |
| 用户系统 | 双 Token 无感认证    | JWT + Redis 缓存刷新机制  |
| 客房展示 | 动态筛选+3D 全景展示 | WebGL 集成+自定义指令封装 |
| 预订系统 | 实时房态日历         | Day.js + 服务端冲突校验   |
| 管理后台 | 数据可视化看板       | ECharts + 定时任务统计    |

---

---

## 快速启动

### 开发模式

#### 前端开发

cd client
npm install
npm run dev

### 后端开发

cd server
pip install -r requirements.txt
python manage.py runserver

### 生产部署

docker-compose up -d --build

### 安全方案

双 Token 轮换机制防止 XSS 攻击
Django 信号机制实现操作审计

### 工程化实践

自定义 Vite 插件实现按需打包
Git Hooks 实现提交前代码校验

### 后续计划

接入微信小程序端
实现智能客房 IoT 控制
增加大数据分析模块
