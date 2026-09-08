---
name: project-ai-hub
description: GitHub 统一 AI 聚合管理平台 ai-hub（中央平台:8000 + 网关实例:3000+），多网关 API 聚合、多引擎 AI 搜索、飞书数据同步
metadata:
  type: project
  node_type: memory
  originSessionId: 72205e30-501c-4c38-91a5-20cf27cb4d60
  modified: 2026-08-19T14:37:44.883Z
---

**GitHub 仓库**：`github.com/201650545/ai-hub`（公开，2026-08-07 创建，Python 主语言；**2026-09-06 已归档只读**）

> **现状（2026-09-06）**：ai-hub 全部工作已并入 `github.com/201650545/ai-platform`（monorepo，tag `monorepo-v1-20260906`）。ai-hub 设为归档只读，仅保留 `main` 分支（含退役说明提交 `5e63c49`）。本仓在线运行体仍位于 `D:\项目\ai-hub\search_gateway` 未迁移。

**定位**：统一 AI 聚合管理平台，面向个人 LAN（最多 50 人共享，简单 token 鉴权）。代码托管在 GitHub，存储为本地 JSON 文件同步到飞书多维表格。

**架构**（5 目录）：
- `00_中央平台/`（FastAPI, port 8000）— 网关注册/发现/统计/飞书同步/管理面板
- `01_网关模板/` — 网关生成器模板
- `02_网关实例/`（port 3000+，如 `ds_v4_cli`）— 运行中的网关实例（含 `unified_gateway.py`）
- `03_共享组件/` — 跨网关共享代码（`history.py`、`quota.py` 等）
- `04_任务卡/` + `05_执行指令/` — 任务跟踪与操作规范

**已完模块**：网关模板、管理面板 UI、飞书同步、GitHub 集成、网关迁移、渠道扩容、多轮对话搜索、E2E 测试套件、GitHub 推送/标准化、对话历史管理、本地配额统计、组件编排核心 + Bilibili 嵌入。剩余编排任务（012/015/016）限定 Gemini。

**使用方式**：
1. `pip install fastapi uvicorn httpx`
2. `cp config/channels.example.json config/channels.json` 填 API key
3. 启动中央平台：`python server.py`（`00_中央平台/`）
4. 启动网关实例：`python unified_gateway.py`（`02_网关实例/ds_v4_cli/`）

访问入口：`localhost:8000`（管理面板）、`localhost:3000`（网关）、`localhost:8000/docs`（API 文档）。

**AI 协作守则**：贡献前按序读 `ARCHITECTURE.md` → `04_任务卡/` → `05_执行指令/`；改完后跑 `python tests/run_all.py` 一键回归。目标环境 Windows + ChatGPT。

## 归档仓库清理记录（2026-09-06）

**背景**：检查 ai-hub 归档仓库是否还残留未合并分支/提交。结论——`refactor/monorepo-20260812`（72 个血缘未合并提交）与 `main`（1 个退役说明提交）。经**内容级**验证（非仅提交血缘）：refactor 分支的核心新文件 `pricing.py` 与 ai-platform main **blob 完全一致**；`capabilities.py`/`resource_config.py` 仅差 16 行且为 **monorepo 路径搬迁**（`services/search_gateway/` → `apps/search-gateway/services/`，相似度 98%），无逻辑差异。即 72 个提交只是 monorepo 合并（PR #1/PR #5）的源历史，内容已全部并入 ai-platform main，**无丢失工作**。

**操作步骤（opencli 解除归档 + 删分支）**：
1. GitHub 归档仓库是**只读**的，`git push --delete` 直接返回 `403`/`This repository was archived so it is read-only`，必须先解除归档。
2. 用 `opencli browser gh-ahub open "https://github.com/201650545/ai-hub/settings"` 打开设置页。归档态下 Danger Zone 显示「Unarchive this repository」。
3. 点按钮弹确认对话框 → `fill 'input[name=verify]' "201650545/ai-hub"`（仓库名验证，`pattern=201650545/[aA][iI]-[hH][uU][bB]`）→ `click 'form[action*="unarchive"] button[type=submit]'` 提交 → 立即 `UNARCHIVED-OK`，**无需密码/2FA**。
4. 回 git：`git push ai-hub --delete refactor/monorepo-20260812` 成功，ai-hub 远端现仅剩 `main`。
5. 本地远程跟踪引用 `refs/remotes/ai-hub/refactor/monorepo-20260812` 用 `git update-ref -d` 清理。

**经验**（复用要点）：
- 判断分支是否「真正丢失工作」要看**内容**而非提交血缘：squash/迁移合并会把源码提交换成新哈希，血缘上算未合并，但 blob 可能完全一致。用 `git rev-parse <ref>:<path>` 对比 blob hash、`git diff --stat` 看差异量级即可判别。
- GitHub 归档仓库要删残留分支：先 opencli 到 `/settings` 解除归档（对话框只需输入仓库名验证，不要求密码/2FA），删完可再归档回去。归档仓库多数设置被隐藏，设危险区操作需解除归档后才显示。

关联：[[project-ai-gateway]] [[project-ai-resource-hub-bridge]] [[project-shared-memory]] [[project-github-sync]]
## 总网关前端 v2 交付（2026-09-06，GPT 镜像 Extended 完成）
- 交付物：D:\项目\services\central\generated\总网关前端_v2\ai-gateway-console-deliverable.zip（解压目录 ai-gateway-console\，含自包含 index.html 437KB、DESIGN.md、README.md、3 主题图标厂牌+背景）
- 已部署：D:\项目\services\central\dashboard\（index.html + assets\，:8000 根路径即新前端）
- 三主题：中式留白 / Swiss 国际主义 / 现代黑白玻璃；九宫格图标按总览/转发/搜索/仓库/表册/在线/离线/设置/关于 切割；含深浅模式、WebAudio 轻音效、10s 网关轮询、旧部署降级
- 协作准则：见 用户/传话筒铁律_与强模型协作准则.md（传话筒不越权，GPT 提问须核实后如实回传）
