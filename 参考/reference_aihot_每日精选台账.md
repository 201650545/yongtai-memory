---
name: reference_aihot_每日精选台账
description: AIHOT 每日本质精选的**去重台账**（事件级条目粒度，滚动 14 天 / ≤30 行）；由 search_gateway\scripts\aihot_daily_store.py 单写，是「最近推过什么」的唯一真源
type: reference
updated: 2026-10-29
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
| 2026-10-23 | [[自动化研究闭环]]进入开源模型 |  | Recursive—— | https://the-decoder.com/recursive-shows-first-result-of-its-ai-driven-research-process-with-flint/ | D:\Work\元智能\20_自适应工作流引擎\runtime\aihot_daily_picks\entries\2026-10-23-01.md |
| 2026-10-23 | [[决策模型]]开始替代规则编排 |  | 蚂蚁数科—— | https://www.ithome.com/1/016/633.htm | D:\Work\元智能\20_自适应工作流引擎\runtime\aihot_daily_picks\entries\2026-10-23-02.md |
| 2026-10-24 | 开放权重压低智能体成本 | 稀疏激活 | MiniMax | https://x.com/MiniMax_AI/status/2113452026902589732 | D:\Work\元智能\20_自适应工作流引擎\runtime\aihot_daily_picks\entries\2026-10-24-01.md |
| 2026-10-24 | 世界模型先做交互分镜 | 世界记忆 | 腾讯混元 | https://x.com/TencentHunyuan/status/2113676827114053892 | D:\Work\元智能\20_自适应工作流引擎\runtime\aihot_daily_picks\entries\2026-10-24-02.md |
| 2026-10-24 | 超小TTS把语音搬回端侧 | 端侧语音合成 | Gradium | https://www.marktechpost.com/2026/10/22/gradium-phonon-31m-on-device-tts/ | D:\Work\元智能\20_自适应工作流引擎\runtime\aihot_daily_picks\entries\2026-10-24-03.md |
| 2026-10-25 | **纯语音模型重定义实时交互** | 纯语音端到端 | Block（） | https://techcrunch.com/2026/10/24/blocks-new-voice-model-sounds-eerily-human/ | D:\Work\元智能\20_自适应工作流引擎\runtime\aihot_daily_picks\entries\2026-10-25-01.md |
| 2026-10-25 | **开放模型应分级解锁能力** | 能力降权发布 | Moonshot AI（） | https://x.com/RohanPaul_ai/status/2113713658887102788 | D:\Work\元智能\20_自适应工作流引擎\runtime\aihot_daily_picks\entries\2026-10-25-02.md |
| 2026-10-26 | **线性注意力降低服务门槛** | 混合专家架构、线性注意力 | KRAFTON AI（） | https://www.ithome.com/1/017/695.htm | D:\Work\元智能\20_自适应工作流引擎\runtime\aihot_daily_picks\entries\2026-10-26-01.md |
| 2026-10-27 | [[代码化视频]]成为可编排中间层 |  | Artificial Analysis |  | D:\Work\元智能\20_自适应工作流引擎\runtime\aihot_daily_picks\entries\2026-10-27-01.md |
| 2026-10-27 | [[实时同传]]打通语音翻译闭环 |  | 腾讯混元 |  | D:\Work\元智能\20_自适应工作流引擎\runtime\aihot_daily_picks\entries\2026-10-27-02.md |
| 2026-10-28 | 长文档解析转向固定成本 | 稀疏参考注意力 | 百度—— | https://www.marktechpost.com/2026/10/26/baidu-unlimited-ocr-2-open-source-long-document-ocr/ | D:\Work\元智能\20_自适应工作流引擎\runtime\aihot_daily_picks\entries\2026-10-28-01.md |
| 2026-10-28 | 流式安全可嵌入推理过程 | 流式安全探针 | 蚂蚁 inclusionAI—— | https://huggingface.co/inclusionAI/Qwen3.8-Flash-Next-singprobe | D:\Work\元智能\20_自适应工作流引擎\runtime\aihot_daily_picks\entries\2026-10-28-02.md |
| 2026-10-29 | 名次是移动靶，改看分差档位 | 跨厂商路由、档位选型 | GitHub（Copilot Fusion）、Artificial Analysis（Index v5、Coding Agent Index v2.0） |  | D:\Work\元智能\20_自适应工作流引擎\runtime\aihot_daily_picks\entries\2026-10-29-01.md |
| 2026-10-29 | 语音四合一，ASR 进免费线 | 开放权重、串行管线塌缩 | NVIDIA（Nemotron 3.5 Transcribe） |  | D:\Work\元智能\20_自适应工作流引擎\runtime\aihot_daily_picks\entries\2026-10-29-02.md |
| 2026-10-29 | 文档解析进端侧，可信度交给小模型 | 端侧解析、可靠性判别 | 面壁智能 OpenBMB（MiniCPM-OCR 1.0 / MiniCPM-OCR Jev） |  | D:\Work\元智能\20_自适应工作流引擎\runtime\aihot_daily_picks\entries\2026-10-29-03.md |
