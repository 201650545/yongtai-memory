---
name: reference_aihot_每日精选台账
description: AIHOT 每日本质精选的**去重台账**（事件级条目粒度，滚动 14 天 / ≤30 行）；由 search_gateway\scripts\aihot_daily_store.py 单写，是「最近推过什么」的唯一真源
type: reference
updated: 2026-10-22
---
# AIHOT 每日精选台账（去重真源）

> **用途**：每天跑「每日本质精选」时，模型与程序都拿它做去重 —— 近期已推过的同一件事不重复推。
> **粒度**：**一条结论一行**（事件级），不是一天一行 —— 合并成一天会把粒度聚合回去，白吃收益。
> **写入方**：`D:\项目\ai-hub\search_gateway\scripts\aihot_daily_store.py`（唯一写入者）。
> **保留**：滚动 14 天 / 最多 30 行；条目的**全文**在 `D:\Work\元智能\20_自适应工作流引擎\runtime\aihot_daily_picks\entries\`，本表只存指针与去重键。

| 日期 | 标题 | 概念 | 出处 | 链接 | 条目文件 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 2026-10-21 | 文档解析进入结构化阶段 |  | SoMark | https://x.com/rohanpaul_ai/status/2112629681765974479 | D:\Work\元智能\20_自适应工作流引擎\runtime\aihot_daily_picks\entries\2026-10-21-01.md |
| 2026-10-21 | 语音链路可独立选型 | 语音转写、语音合成 | Mistral AI | https://x.com/MistralAI/status/2112574615318876178 | D:\Work\元智能\20_自适应工作流引擎\runtime\aihot_daily_picks\entries\2026-10-21-02.md |
| 2026-10-21 | 设计生成转向可编辑交付 | 原生图层 | Coco Labs | https://x.com/rohanpaul_ai/status/2112635536326512771 | D:\Work\元智能\20_自适应工作流引擎\runtime\aihot_daily_picks\entries\2026-10-21-03.md |
| 2026-10-22 | 投机解码提升免费线吞吐 | 投机解码 | inclusionAI —— | https://huggingface.co/inclusionAI/Ling-3.0-tiny-UBTree | D:\Work\元智能\20_自适应工作流引擎\runtime\aihot_daily_picks\entries\2026-10-22-01.md |
| 2026-10-22 | 本地图像生成跨过显存门槛 | 消费级本地生图 | Black Forest Labs —— | https://www.ithome.com/1/016/062.htm | D:\Work\元智能\20_自适应工作流引擎\runtime\aihot_daily_picks\entries\2026-10-22-02.md |
| 2026-10-22 | 检索链应拆成召回与重排 | 检索分层 | NVIDIA —— | https://huggingface.co/blog/nvidia/nemotron-retriever-world-class-agentic-retrieval | D:\Work\元智能\20_自适应工作流引擎\runtime\aihot_daily_picks\entries\2026-10-22-03.md |
