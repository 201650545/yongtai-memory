---
name: AGENTS
type: entry
updated: 2026-10-22
kind: fact
status: active
---
# 本仓只给 AI 读

第一动作：读 `D:\记忆\README.md`（机器契约，90 行）。
要看体系结构：`D:\记忆\SYSTEM_MAP.md`。
要找东西：`D:\记忆\q.cmd "关键词"`（跨 Work 加 `--work "D:\Work"`）。

不要整本读笔记；不要问用户"哪个仓库"；索引是生成物，禁手改。

## 检索硬约束（不要整本读，烧代理流量）

- 查任何东西先跑 `D:\记忆\q.cmd "关键词"`，跨库加 `--work "D:\Work"`；**禁止整篇读笔记**（含本文件、`项目\project_想法池.md`、`索引.md`）。
- 要精读某一节：先跑 `locate_anchor.py "<文件>" "<章节>"` 取行号（脚本在 `D:\Work\元智能\10_AI自成长引擎\技能库\local-knowledge-engine\scripts\`），再只读该区间（≤50 行）。
- 机制正文在 `C:\Users\郭永涛\AGENTS.md` 第 7 条，此处只放指针，不复制正文（单写真源）。
