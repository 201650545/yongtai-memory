---
name: shared-memory-repo
description: 多 Agent 共享记忆仓库 ai-hub-memory（分层协议），执行前读 STATE/DECISIONS、做完写 CHANGELOG
metadata: 
  node_type: memory
  type: project
  originSessionId: 95cff9f0-c115-4770-a66a-5ed8ec23a5c2
  modified: 2026-08-13T11:11:53.473Z
---

多 Agent 共享记忆系统（2026-08-13 上线）：GitHub 公开仓库 **https://github.com/201650545/ai-hub-memory**，本地 `D:\项目\ai-hub-memory`。

4 文件分层：AGENTS.md（协作协议+工具地图+并发规则）、STATE.md（当前状态，整体覆盖不追加）、DECISIONS.md（决策，追加）、CHANGELOG.md（操作记录，追加）。

协作协议：执行前先读 STATE.md + DECISIONS.md；做完在 CHANGELOG.md 追加一条；用户敲板追加进 DECISIONS.md。GPT 两条纠正已写入：① append-only 不免疫冲突 → 不同 Agent 不改同一文件；② 协议只做引导、强制靠 hook。

关联 [[on-demand-orchestration]] [[ai-gateway]]。
