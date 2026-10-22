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

## 两条最常踩的坑（新 Agent 先看）

- **要出图/画图/配图/封面/插图/图标**：先读 `反馈/feedback-有生图模型就别用代码画图.md`。本机生图渠道很多（`:3100` 的 `image-gen`、ChatGPT 镜像 skill、豆包/元宝网页版），**非必要不要手写 SVG/PIL/matplotlib 画图**（丑且能力差），生成的图也不要带水印。
- **要改记忆库**：`索引.md` 是生成物、**禁止手改**。改完条目后跑 `cd D:\Work\元智能\runners; python build_memory_index.py --build` 重建；体检用 `--check`；**`--migrate` 会原地改条目原文，别乱跑**。
