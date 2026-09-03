---
name: project-feishu-data-hub
description: GitHub Pages 公开数据枢纽 feishu-data-hub —— 飞书多维表格 → 静态 JSON，为 AI 工具提供可读的非结构化数据
metadata:
  type: project
  node_type: memory
  originSessionId: 72205e30-501c-4c38-91a5-20cf27cb4d60
  modified: 2026-08-19T14:37:44.941Z
---

**GitHub 仓库**：`github.com/201650545/feishu-data-hub`（公开，2026-07-25 创建，JavaScript 主语言）

**站点**：https://201650545.github.io/feishu-data-hub/

**定位**：统一公开导出的飞书多维表格数据中心。将飞书 Base 记录导出为静态 JSON，部署到 GitHub Pages，AI 工具和其他消费者无需飞书权限即可读取数据模型、记录和表关联。

**架构**：单仓库多项目——飞书 Base → `sync-project.mjs` → `public/projects/<slug>/` → `catalog.json` → GitHub Pages。故障隔离（正常故障只影响单个项目，安全故障终止整个部署），旧 URL 兼容（`mirror_to_legacy_root`），cache busting（`build_id` + `?v=<build_id>`）。

**公开端点**：
- `/catalog.json` — 全局目录索引
- `/index.html` — 可读首页
- `/projects/<slug>/manifest.json`、`schema.json`、`status.json`、`index.html` — 项目级数据
- `/data/manifest.json` 和 `/data/schema.json` — 旧版兼容（`learning-english`）

**当前项目**：`learning-english`（英语学习系统）— 4 张表，6,131 条记录（文本库 30、词汇/轻量记录 6,000、学习日志 92、日计划 9）。

**三层安全**：
1. 视图层：仅导出 `AI 公开导出` 视图
2. 字段层：显式白名单，无通配符，敏感字段名拦截
3. 内容层：写入时+部署前双重模式扫描，凭据泄露终止部署

**CI/CD**：4 个 GitHub Actions（sync-hourly/daily/manual/validate），全固定 commit SHA，每周 Dependabot。流程：checkout → Node 22 → npm ci → 语法/配置检查 → 同步 → 输出校验 → 安全扫描 → 部署。

**新增项目流程**：在飞书 Base 建 `AI 公开导出` 视图 → 授权统一飞书应用只读 → 更新 GitHub Secret → `npm run project:add -- --slug <slug> --title "..." --base-key <key>` → 配置 YAML 白名单 → dry-run → 安全扫描 → 手动部署。

关联：[[reference-feishu-app-qclaw]] [[project-ai-resource-hub-bridge]] [[project-ai-hub]]