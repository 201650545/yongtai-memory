---
name: project-ai-hub
description: GitHub 统一 AI 聚合管理平台 ai-hub（中央平台:8000 + 网关实例），多网关 API 聚合、飞书数据同步；2026-09-06 已归档只读，工作并入 ai-platform monorepo。
metadata:
  type: project
  node_type: memory
  originSessionId: 72205e30-501c-4c38-91a5-20cf27cb4d60
  modified: 2026-09-08T00:00:00.000Z
type: project
updated: 2026-10-19
kind: fact
status: active
scope: ai_hub
---

# AI Hub 聚合平台（ai-hub · 已并入 ai-platform）

> 本页为**概述 + 时间线索引**。操作级/过程性详情已归档至
> 👉 `项目/归档/project_ai_hub_完整详细记录.md`（2026-09-08 起，本页只留结论，避免臃肿）。

## 这是什么

统一 AI 聚合管理平台，面向个人 LAN（≤50 人共享，简单 token 鉴权）。代码托管 GitHub，存储为本地 JSON 同步到飞书多维表格。

## 现状（关键）

- **GitHub 仓库**：`github.com/201650545/ai-hub`（公开，2026-08-07 创建，**已于 2026-09-06 归档只读**，仅剩 `main` 含退役说明提交 `5e63c49`）。
  - **⚠️ 2026-10-10 实测补充**：该地址现已**返回 404，无法访问**（跟随重定向后仍为原地址，可排除"改名"；删除或转私有从外部无法区分）。`git push` 报 `Repository not found`。
    上面"已归档只读"是 2026-09-06 的历史状态，**不是当前状态**——归档的仓不会 404。
    此前"推不上去"类故障请先查这一条，不要再去试 unarchive。
  - **⚠️ 2026-10-19 再核实**：`origin`（ai-hub.git）与 `platform`（ai-platform.git）**两个 remote 全部 Repository not found**。
    本地 116 个提交、44 个未推送 ⇒ **从 9-05 起本地与 GitHub 彻底分家，此后再没同步过**。
    本地单机演进是当前唯一现实，**不要再尝试 push**。
- **工作已并入**：`github.com/201650545/ai-platform`（monorepo，tag `monorepo-v1-20260906`）。ai-hub 归档前的内容（架构 5 目录、已完模块、网关迁移等）已全部并入，**无丢失工作**。
- **在线运行体**：仍位于 `D:\项目\ai-hub\search_gateway` 未迁移。
  - 🔴 **2026-10-19 重大澄清**：`projects.yaml` 的 `ai-platform` 条目曾写「本地目录已物理删除」，
    **这与事实严重不符，害我差点误删运行体**。实测该目录是**本机命脉、仍在活跃服务**：
    `:3100`（nssm `ai-gateway-3100`）与 `:8787`（实测 6 个活跃连接）均在监听，
    另有 **15 个计划任务**挂在它身上（渠道刷新 / 席位编排 / 网关测速 / AA 与 AIHOT 榜单快照 / 快照自动提交等）。
    ⇒ **禁止删除、禁止移动该目录**；`projects.yaml` 已新增 `ai-hub` 条目（status: active）改正此口径。
    `D:\Work\API转发网关` 只是它的**文档仓**，不是运行体。

## 时间线（近→远）

- **2026-09-06 · 总网关前端 v2 交付**（GPT 镜像 Extended）：deliverable 解压至 `D:\项目\services\central\generated\总网关前端_v2\`，已部署 :8000 root。三主题（中式留白/Swiss 国际主义/现代黑白玻璃），含深浅模式、WebAudio、10s 网关轮询。协作准则见 `用户/传话筒铁律_与强模型协作准则.md`。
- **2026-09-06 · 归档 + 仓库清理**：ai-hub 并入 monorepo 后设为归档只读；清理 `refactor/monorepo-20260812`（72 血缘未合并提交，但 blob 内容已并入，无丢失）——opencli 到 `/settings` 解除归档 → 删分支 → 再归档。

## 架构（并入前，5 目录）

`00_中央平台/`（FastAPI :8000，网关注册/发现/统计/飞书同步/管理面板）、`01_网关模板/`、`02_网关实例/`（如 ds_v4_cli）、`03_共享组件/`（history/quota）、`04_任务卡/` + `05_执行指令/`。

## 源文件

- 完整详细记录（架构/已完模块/使用方式/归档清理操作步骤与经验/v2 交付明细）→ `项目/归档/project_ai_hub_完整详细记录.md`
- 关联条目：[[project_ai_gateway]] [[project_ai_resource_hub_bridge]] [[project_shared_memory]] [[project_github_sync]]