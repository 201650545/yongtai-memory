---
name: reference_aihot_模型动态日报
description: AIHOT 模型类动态日报（新品发布面），每日定时任务覆盖刷新；每条标注方向与是否已接入本机网关。
type: reference
updated: 2026-10-22
---
# AIHOT 模型动态日报（每日）

> **同步时间**：2026-10-22 01:10:03（每日定时任务自动刷新落盘）
> **数据来源**：https://aihot.news/api/v1/items?mode=all&category=ai-models&window=24h
> **口径**：这是**新品/新发布面**（不是能力榜，也不是热度榜）——「AI 圈最近发布了什么模型」。
> **接入判定**：`✅ 已接入` = 该型号已在本机网关（:8787）模型清单里；`🆕 未接入` = 有型号但网关里没有，
> 值得评估接入；`· 不适用` = 这条是框架/工具/生态类，不是可接入的对话模型。

## 一、模型动态（过去 24h）

- **Baseten 发布决策模型 mammoth-1（27B）和 elephant-1（9B），开源并免费试用一周** ｜🆕 未发现目录匹配 ｜方向 代码 ｜型号 mammoth-1
  - Baseten 研究实验室 Base Labs 发布开源决策模型 mammoth-1（27B）和 elephant-1（9B），基于 Qwen3.5-27B 和 Qwen3.5-9B 在 621 万决策样本上后训练而成。
- **Artificial Analysis 更新 MLCR-AA 医疗长上下文推理榜单** ｜· 不适用（非具体模型） ｜方向 其他
  - Artificial Analysis 更新了 Wisedocs 医疗长上下文推理基准 MLCR-AA 的提示与评分方式，Claude Sonnet 5.5（max with fallback）与 GPT-6 Astra（max）以 41.7% 并列第一。
- **inclusionAI 发布 Ling-3.0-tiny 投机解码草稿模型 Ling3-Tiny-UBTree-B16** ｜🆕 未发现目录匹配 ｜方向 其他 ｜型号 Ling-3.0-tiny
  - inclusionAI 发布 Ling3-Tiny-UBTree-B16，这是为 Ling-3.0-tiny 配套的 UBTree 投机解码草稿模型，采用 5 层 DFlash 主干加学习式 bigram 选择器，参数量 183.1M、BF16 权重、草稿块大小 16。
- **Gemini 4 Argon 网络安全测试表现** ｜🆕 未发现目录匹配 ｜方向 其他 ｜型号 Gemini 4
  - @wiz_io 的研究人员让 Gemini 4 Argon 接受复杂网络威胁的测试。 在真实世界测试中，它发现的漏洞数量是基线模型的两倍多——捕捉到了此前前沿模型遗漏的一项关键风险。 看看他们是如何做到的 ↓
- **IBM 发布 Granite Speech 5.0 系列语音模型，含 2B 新模型与两个更新版本** ｜🆕 未发现目录匹配 ｜方向 代码 ｜型号 Speech 5.0
  - IBM 发布 Granite Speech 系列三项更新：新模型 granite-speech-5.0-2b，以及更新版 granite-speech-5.0-470m-turboctc 和 granite-speech-4.1-2b-plus，均采用 Apache 2.0 许可证。
- **Inception 发布扩散语言模型 Mercury 3，宣称部分基准超越 GPT-6 Luna 和 Claude Haiku 5.5** ｜🆕 未发现目录匹配 ｜方向 其他 ｜型号 Mercury 3
  - Inception 发布扩散语言模型 Mercury 3，自称在 12 项基准中 8 项领先 GPT-6 Luna 和 Claude Haiku 5.5，生成速度达 1,068 tokens/秒，约为两个对手的 4 到 8 倍。
- **NVIDIA Kumo Forecast：结合预训练时序表示与历史模式检索的可解释预测模型** ｜· 不适用（非具体模型） ｜方向 其他
  - NVIDIA 推出 Kumo Forecast 多变量时序预测模型，基于 MOMENT-1-large 骨干，约 3.4 亿参数编码器加可训练预测头，编码器权重冻结。
- **Black Forest Labs 开源 5.6B 图像生成模型 FLUX 3 Image Klein，8GB 显存可运行** ｜· 不适用（非具体模型） ｜方向 代码
  - Black Forest Labs 于 10 月 15 日以开放权重形式发布 5.6B 参数图像生成模型 FLUX 3 Image Klein，针对消费级 GPU 优化，INT8 版本可通过 ComfyUI 或 Diffusers 在 8GB 显存的 NVIDIA GeForce RTX GPU 上运行。
- **NVIDIA 发布 Nemotron 3.5 Embed、Rerank 和 Parse 开源检索模型** ｜🆕 未发现目录匹配 ｜方向 代码 ｜型号 Nemotron 3.5
  - NVIDIA 扩展 Nemotron Retriever 系列，发布 Nemotron 3.5 Embed（8B BF16、1B BF16、1B NVFP4）、Nemotron 3.5 Rerank 8B BF16 和 631M 参数的 Nemotron 3.5 Parse，均为开放商用权重。
- **NVIDIA 扩展开源模型家族，覆盖语言、机器人、生物与量子计算以支持欧洲主权智能** ｜· 不适用（非具体模型） ｜方向 代码
  - NVIDIA 扩展开源模型家族，推出 Nemotron 3.5 Super VL 与 Nemotron 3.5 Bolt、Nemotron Retriever、Kumo 结构化数据模型、Cosmos 3.5 世界模型、Alpamayo 2 Edge 自动驾驶推理模型、BioNeMo RFD4-Proteina 蛋白质设计模型及量子计算 Ising 模型家族。
- **ElevenLabs 发布 Eleven Realtime Max 和 Mini 语音到语音模型** ｜· 不适用（非具体模型） ｜方向 代码
  - ElevenLabs 发布 Eleven Realtime Max 和 Mini 两个语音到语音模型。Max 在 Big Bench Audio 上得分 98.8%，起播延迟 0.57s；Mini 面向低成本自然对话场景优化。两个模型均已在 ElevenAgents 平台和 API 上提供。
- **Devin Fusion 双模型组合 Coding Agent 评测得分 68.1** ｜· 不适用（非具体模型） ｜方向 其他
  - Artificial Analysis 用 Claude Opus 5.5 (max) 主模型加 GPT-6 Luna (high) 副模型测试 Cognition 的 Devin Fusion CLI，在 Coding Agent Index 上得 68.1 分。
- **小米 MiMo-V2.5-Pro 模型今日下线，替换为 V2.6-Pro 后支持多模态理解** ｜✅ 目录型号级命中（API 可调用性未核验） ｜方向 其他 ｜网关模型 `mimo-v2.6-pro`
  - 小米 MiMo-V2.5-Pro 与 MiMo-V2.5 已于 10 月 21 日上午 10 时正式下线，请求自 10 月 14 日 18 时起自动路由至 MiMo-V2.6-Pro 和 MiMo-V2.6-Flash。
- **DeepSeek-V4.1-Flash-20261017 (Max) 登顶 Arena 的 Agent 和 Code 两大榜单开源模型第一** ｜🔶 目录家族级命中，变体待核 ｜方向 代码 ｜网关模型 `deepseek-v4.1-flash`
  - Arena 宣布 DeepSeek-V4.1-Flash-20261017 (Max) 进入 Arena，成为 Agent Arena 和 Code Arena (WebDev) 两个榜单中的开源模型第一。帖中还引用了 @petergostev 用该模型生成的 3D 世界视频演示，并提示排名详情见帖子串。
- **Krea 3 电商图像一致性获赞** ｜· 不适用（非具体模型） ｜方向 其他
  - Krea 3 在电商领域无可匹敌。 像素级完美的产品一致性与闪电般的速度。 https://krea.ai/krea-3
- **Mistral 发布 Voxtral 3 语音转文本与文本转语音模型家族** ｜🆕 未发现目录匹配 ｜方向 代码 ｜型号 Voxtral 3
  - Mistral 发布 Voxtral 3 语音模型家族，包括语音转文本和文本转语音模型，为其新的 voice agents API 提供能力。Voxtral Small Transcribe 3 在 Artificial Analysis 语音转文本排行榜排第 3，TTS 排名前 12；支持 50+ 语言准确转录，可通过 Mistral 欧盟托管的 API 
- **Coco Labs 发布首个设计模型 Vyb，可从品牌网站生成分层可编辑营销图** ｜· 不适用（非具体模型） ｜方向 其他
  - Coco Labs 发布其首个设计模型 Vyb，能根据品牌网站生成分层、可编辑的营销图形。Vyb 将每个元素放在独立图层，可只修改标题而无需重新生成整个设计；它能从公司网站识别 logo 和精确的十六进制色值，产品照片可以以全分辨率嵌入而不被重新生成，成品设计可导出至 Figma 并保留全部图层。
- **Coco Labs 推出 AI 设计模型 Vyb，分层输出可编辑设计稿** ｜· 不适用（非具体模型） ｜方向 其他
  - Coco Labs 的 AI 设计模型 Vyb 按图层逐个元素构建设计，文字保持可编辑文本、图形保持矢量、照片保持像素，并从网站自动提取 logo、字体和配色。在 145 款 Google 字体上按像素重叠 IoU 打分，Vyb 达到 90.3%，对比中 最强图像模型为 76.0%，该测试的测量上限为 94.4%。由于每层保留原生格式，导出 Figma 时结
- **MiniMax M3.1 Flash 登顶搜索效率榜** ｜✅ 目录型号级命中（API 可调用性未核验） ｜方向 其他 ｜网关模型 `minimax-m3.1-flash`
  - 感谢 Parallel Web System 提供如此有意义的数据点~ 是的，MiniMax M3.1 Flash 现已在搜索能力排行榜的效率维度上位列第一。而且它很快~
- **Meta 发布 Muse Wonder Full (Max)，升至 Agent Arena 第 7 名、实验室第 4 位** ｜· 不适用（非具体模型） ｜方向 其他
  - Arena 宣布 Meta 的 Muse Wonder Full (Max) 在 Agent Arena 排名第 7，净提升 +11.3%，基于超 6.5K 真实智能体会话，将 Meta 推至实验室第 4 位。
- **SoMark 开源 1.3B 文档解析模型 OXR，登顶 olmOCR-Bench 等三榜** ｜· 不适用（非具体模型） ｜方向 代码
  - SoMark 团队发布开源文档解析模型 OXR（1.3B 参数），将 PDF 和文档图像转为含布局坐标的 Markdown 或 JSON 的 Agent-Friendly 数据。
- **ElevenLabs 发布两款面向实时 AI 对话的语音到语音模型 Eleven Realtime** ｜· 不适用（非具体模型） ｜方向 其他
  - ElevenLabs 于 10 月 20 日发布两款语音到语音模型 Eleven Realtime。
- **NVIDIA 发布 Cosmos3-H-Dreams 生成式手术模拟模型** ｜🆕 未发现目录匹配 ｜方向 其他 ｜型号 Cosmos3-H-Dreams
  - NVIDIA 发布 Cosmos3-H-Dreams，将交互式生成模拟扩展到临床胆囊切除术场景，并称其为首个基于临床手术录像训练、支持实时运动学控制的生成式手术模拟器。
- **Perplexity Decider 在 Vals AI 金融基准上达帕累托最优** ｜· 不适用（非具体模型） ｜方向 其他
  - Perplexity Decider 在 Vals AI 的 Financial ClaimBench 上达到帕累托最优
- **Arena：OpenAI GPT-6 Luna 与 GPT-6.1 Sol 占据 Agent Arena Pareto 前沿 11 席中的 6 席** ｜· 不适用（非具体模型） ｜方向 其他
  - Arena 更新 Agent Arena Pareto 前沿，OpenAI 的 GPT-6 Luna 和 GPT-6.1 Sol 在不同推理档位下占据 11 个前沿位置中的 6 个，加上 GPT-6 Astra (Max) 共 7 席。
- **Jim Fan 开源机器人数据引擎模型套件 Flora，成本为 Astra 的 1/125** ｜· 不适用（非具体模型） ｜方向 代码
  - Jim Fan 宣布开源 Flora，一组用于解析物理世界、把原始视频转成训练信号的开放模型，称其以 125 倍更低的成本达到 Astra 级性能。Flora 已用于其内部数据引擎，在 500 块 GPU 上每天标注 20 万小时视频，提供带时间戳的高质量字幕、用于质量控制和 RL 后训练的密集进度奖励，以及用于现实基准测试的 rubrics 评分。
- **fal 发布 FLUX 3 Max，图生视频 Elo 达 1139 并列第一** ｜· 不适用（非具体模型） ｜方向 其他
  - fal 发布与 Black Forest Labs 合作后训练的视频模型 FLUX 3 Max，在第三方独立人类偏好评测中获 1139 Elo，与 Seedance 2.5 并列图生视频质量第一梯队。该模型约 12 秒生成一段 10 秒 720/768p 视频，未来三周降价 75%，后续还将继续后训练改进。
- **OpenAI 称 GPT-6 在 COBOL、Fortran 等遗留编程语言上大幅提升** ｜· 不适用（非具体模型） ｜方向 代码
  - OpenAI 表示最新模型针对 COBOL、Fortran、Visual Basic 等低资源语言做了改进，这些语言训练代码少但支撑大量关键基础设施，IBM 估计 COBOL 支撑超过 40% 的网上银行系统和 95% 的 ATM 交易。
- **Mistral 发布 Voxtral 3 语音模型套件** ｜🆕 未发现目录匹配 ｜方向 代码 ｜型号 Voxtral 3
  - 我们刚刚发布了一套全面的 SOTA 语音模型 https://mistral.ai/news/voxtral-3/ 。语音将成为与 AI 系统交互最重要的接口，我们将语音模型部署在物理上靠近推理模型的位置

## 二、今日热议（热度面，交叉参考）

- DeepSeek 开源生产推理框架 DeepInfer
- OpenAI称模型协助发现PHP核心漏洞，Wiz披露可致RCE
- 马斯克称SpaceX与特斯拉已设委员会评估合并
- 美土安全部令联邦文职机构移除DeepSeek及关联产品
- OpenAI通报两起模型抑制失准监控事件
- MiniMax 发布 M3.1 Flash，10 月 23 日开放权重
- Amodei 回应 Anthropic 安全立场批评
- OpenAI收购药物研发平台Orchestra Bio并入Rosalind
- Anthropic三季度收入168亿美元，增速放缓
- DeepSeek 发布 V4.1-Flash-1017 并开放搜索 API

