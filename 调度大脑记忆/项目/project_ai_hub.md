---
name: project-ai-hub
description: GitHub 统一 AI 聚合管理平台 ai-hub（中央平台:8000 + 网关实例:3000+），多网关 API 聚合、多引擎 AI 搜索、飞书数据同步
metadata:
  type: project
  node_type: memory
  originSessionId: 72205e30-501c-4c38-91a5-20cf27cb4d60
  modified: 2026-08-19T14:37:44.883Z
---

**GitHub 仓库**：`github.com/201650545/ai-hub`（公开，2026-08-07 创建，Python 主语言）

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

关联：[[project-ai-gateway]] [[project-ai-resource-hub-bridge]] [[project-shared-memory]]