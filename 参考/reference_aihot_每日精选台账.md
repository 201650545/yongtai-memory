---
name: reference_aihot_每日精选台账
description: AIHOT 每日本质精选的**去重台账**（事件级条目粒度，滚动 14 天 / ≤30 行）；由 search_gateway\scripts\aihot_daily_store.py 单写，是「最近推过什么」的唯一真源
type: reference
updated: 2026-11-04
---
# AIHOT 每日精选台账（去重真源）

> **用途**：每天跑「每日本质精选」时，模型与程序都拿它做去重 —— 近期已推过的同一件事不重复推。
> **粒度**：**一条结论一行**（事件级），不是一天一行 —— 合并成一天会把粒度聚合回去，白吃收益。
> **写入方**：`D:\项目\ai-hub\search_gateway\scripts\aihot_daily_store.py`（唯一写入者）。
> **保留**：滚动 14 天 / 最多 30 行；条目的**全文**在 `D:\Work\元智能\20_自适应工作流引擎\runtime\aihot_daily_picks\entries\`，本表只存指针与去重键。

| 日期 | 标题 | 概念 | 出处 | 链接 | 条目文件 |
| :--- | :--- | :--- | :--- | :--- | :--- |
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
| 2026-10-30 | 语音对齐从转写中拆出 | 逐字高亮 | ElevenLabs（） | https://x.com/ElevenLabs/status/2115527286065914248 | D:\Work\元智能\20_自适应工作流引擎\runtime\aihot_daily_picks\entries\2026-10-30-01.md |
| 2026-10-30 | 扩散语言模型可端侧跑 | 扩散语言模型、多轮迭代 | DiffuSpace（） | https://www.ithome.com/1/019/783.htm | D:\Work\元智能\20_自适应工作流引擎\runtime\aihot_daily_picks\entries\2026-10-30-02.md |
| 2026-10-31 | 循环共享参数，小模型打大模型 | 循环共享参数、当班模型 | 商汤 SenseTime |  | D:\Work\元智能\20_自适应工作流引擎\runtime\aihot_daily_picks\entries\2026-10-31-01.md |
| 2026-10-31 | 八步 LoRA 改写视频成本线 | 步数蒸馏 | Video Rebirth |  | D:\Work\元智能\20_自适应工作流引擎\runtime\aihot_daily_picks\entries\2026-10-31-02.md |
| 2026-10-31 | 技能市场已是供应链攻击面 | 供应链攻击面 | Cursor（扩展市场通报） |  | D:\Work\元智能\20_自适应工作流引擎\runtime\aihot_daily_picks\entries\2026-10-31-03.md |
| 2026-11-01 | 世界模型转身成智能体训练场 | 交互式模拟、技能自检 | Google DeepMind（原文：） | https://x.com/Google/status/2116237215026032872 | D:\Work\元智能\20_自适应工作流引擎\runtime\aihot_daily_picks\entries\2026-11-01-01.md |
| 2026-11-01 | 抓取退出信号开始统一 | 退出开关、采集链 | OpenAI 等四家 AI 公司 |  | D:\Work\元智能\20_自适应工作流引擎\runtime\aihot_daily_picks\entries\2026-11-01-02.md |
| 2026-11-01 | 本地推理卡在内存带宽 | 内存带宽、当班模型 | Sam Altman（OpenAI），经 The Verge 报道 |  | D:\Work\元智能\20_自适应工作流引擎\runtime\aihot_daily_picks\entries\2026-11-01-03.md |
| 2026-11-02 | OpenAI 12月起将ChatGPT与Codex合并为统一Token额度 |  | 公众号 | https://mp.weixin.qq.com/s?__biz=MzIyMzA5NjEyMA%3D%3D&mid=2647688028&idx=1&sn=e509269da2e0e0b4d4dfbb121b42204b | D:\Work\元智能\20_自适应工作流引擎\runtime\aihot_daily_picks\entries\2026-11-02-01.md |
| 2026-11-02 | OpenRouter 教程：用 Responses API 构建可在 Linux |  | OpenRouter | https://openrouter.ai/blog/tutorials/ai-code-review/ | D:\Work\元智能\20_自适应工作流引擎\runtime\aihot_daily_picks\entries\2026-11-02-02.md |
| 2026-11-02 | 美国白宫科技顾问萨克斯称 Anthropic 可能成为资本主义史上最伟大企业 |  | IT之家 | https://www.ithome.com/1/020/633.htm | D:\Work\元智能\20_自适应工作流引擎\runtime\aihot_daily_picks\entries\2026-11-02-03.md |
| 2026-11-03 | 1-bit 量化可当免费线主力 | 1-bit 量化、内存带宽 | Unsloth（基于 DeepSeek-V4.1-Flash）—— | https://x.com/UnslothAI/status/2117266365929365525 | D:\Work\元智能\20_自适应工作流引擎\runtime\aihot_daily_picks\entries\2026-11-03-01.md |
| 2026-11-03 | 执行环境内嵌进模型权重 | 权重内运行时、工具调用 | Vixhal（独立开发者，MIT 许可发布）—— | https://www.marktechpost.com/2026/11/01/qwengpu-simt-gpu-compiled-into-qwen3-5-2b-weights-runs-cuda/ | D:\Work\元智能\20_自适应工作流引擎\runtime\aihot_daily_picks\entries\2026-11-03-02.md |
| 2026-11-04 | 评测分差来自脚手架而非模型 | 脚手架、候选池 | ARC Prize |  | D:\Work\元智能\20_自适应工作流引擎\runtime\aihot_daily_picks\entries\2026-11-04-01.md |
| 2026-11-04 | 智能体成本大头在重复读 | 上下文复述、前缀缓存 | Arena |  | D:\Work\元智能\20_自适应工作流引擎\runtime\aihot_daily_picks\entries\2026-11-04-02.md |
| 2026-11-04 | 设计交付物升级为可编辑中间层 | 可编辑中间层、免费线 | 商汤 SenseTime |  | D:\Work\元智能\20_自适应工作流引擎\runtime\aihot_daily_picks\entries\2026-11-04-03.md |
