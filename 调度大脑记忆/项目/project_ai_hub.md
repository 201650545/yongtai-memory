---
name: project-ai-hub
description: GitHub 统一 AI 聚合管理平台 ai-hub（中央平台:8000 + 网关实例:3000+），多网关 API 聚合、多引擎 AI 搜索、飞书数据同步；2026-09-06 已归档只读，工作并入 ai-platform monorepo
metadata:
  type: project
  node_type: memory
  originSessionId: 72205e30-501c-4c38-91a5-20cf27cb4d60
  modified: 2026-09-08T00:00:00.000Z
---

# AI Hub 聚合平台（ai-hub · 已并入 ai-platform）

> 本页为**概述 + 时间线索引**。操作级/过程性详情已归档至
> 👉 `项目/归档/project_ai_hub_完整详细记录.md`（2026-09-08 起，本页只留结论，避免臃肿）。

## 这是什么

统一 AI 聚合管理平台，面向个人 LAN（≤50 人共享，简单 token 鉴权）。代码托管 GitHub，存储为本地 JSON 同步到飞书多维表格。

## 现状（关键）

- **GitHub 仓库**：`github.com/201650545/ai-hub`（公开，2026-08-07 创建，**已于 2026-09-06 归档只读**，仅剩 `main` 含退役说明提交 `5e63c49`）。
- **工作已并入**：`github.com/201650545/ai-platform`（monorepo，tag `monorepo-v1-20260906`）。ai-hub 归档前的内容（架构 5 目录、已完模块、网关迁移等）已全部并入，**无丢失工作**。
- **在线运行体**：仍位于 `D:\项目\ai-hub\search_gateway` 未迁移。

## 时间线（近→远）

- **2026-09-06 · 总网关前端 v2 交付**（GPT 镜像 Extended）：deliverable 解压至 `D:\项目\services\central\generated\总网关前端_v2\`，已部署 :8000 root。三主题（中式留白/Swiss 国际主义/现代黑白玻璃），含深浅模式、WebAudio、10s 网关轮询。协作准则见 `用户/传话筒铁律_与强模型协作准则.md`。
- **2026-09-06 · 归档 + 仓库清理**：ai-hub 并入 monorepo 后设为归档只读；清理 `refactor/monorepo-20260812`（72 血缘未合并提交，但 blob 内容已并入，无丢失）——opencli 到 `/settings` 解除归档 → 删分支 → 再归档。
- **2026-08-07 · 创建**：GitHub 建仓 ai-hub，Python 主语言；中央平台 :8000 + 网关实例 :3000 起步。

## 架构（并入前，5 目录）

`00_中央平台/`（FastAPI :8000，网关注册/发现/统计/飞书同步/管理面板）、`01_网关模板/`、`02_网关实例/`（:3000+，如 ds_v4_cli）、`03_共享组件/`（history/quota）、`04_任务卡/` + `05_执行指令/`。

## 源文件

- 完整详细记录（架构/已完模块/使用方式/归档清理操作步骤与经验/v2 交付明细）→ `项目/归档/project_ai_hub_完整详细记录.md`
- 关联条目：[[project_ai_gateway]] [[project_ai_resource_hub_bridge]] [[project_shared_memory]] [[project_github_sync]]