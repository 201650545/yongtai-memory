---
name: reference_aihot_模型动态日报
description: AIHOT 模型类动态日报（新品发布面），每日定时任务覆盖刷新；每条标注方向与是否已接入本机网关。
type: reference
updated: 2026-10-21
---
# AIHOT 模型动态日报（每日）

> **同步时间**：2026-10-21 08:51:59（每日定时任务自动刷新落盘）
> **数据来源**：https://aihot.news/api/v1/items?mode=all&category=ai-models&window=24h
> **口径**：这是**新品/新发布面**（不是能力榜，也不是热度榜）——「AI 圈最近发布了什么模型」。
> **接入判定**：`✅ 已接入` = 该型号已在本机网关（:8787）模型清单里；`🆕 未接入` = 有型号但网关里没有，
> 值得评估接入；`· 不适用` = 这条是框架/工具/生态类，不是可接入的对话模型。

## 一、模型动态（过去 24h）

- **DeepSeek-V4.1-Flash-20261017 (Max) 登顶 Arena 的 Agent 和 Code 两大榜单开源模型第一** ｜✅ 已接入 ｜方向 代码 ｜网关模型 `qwenwork/flash`
  - Arena 宣布 DeepSeek-V4.1-Flash-20261017 (Max) 进入 Arena，成为 Agent Arena 和 Code Arena (WebDev) 两个榜单中的开源模型第一。帖中还引用了 @petergostev 用该模型生成的 3D 世界视频演示，并提示排名详情见帖子串。
- **Krea 3 电商图像一致性获赞** ｜· 不适用 ｜方向 其他
  - Krea 3 在电商领域无可匹敌。 像素级完美的产品一致性与闪电般的速度。 https://krea.ai/krea-3
- **Mistral 发布 Voxtral 3 语音转文本与文本转语音模型家族** ｜🆕 未接入 ｜方向 代码 ｜型号 Voxtral 3
  - Mistral 发布 Voxtral 3 语音模型家族，包括语音转文本和文本转语音模型，为其新的 voice agents API 提供能力。Voxtral Small Transcribe 3 在 Artificial Analysis 语音转文本排行榜排第 3，TTS 排名前 12；支持 50+ 语言准确转录，可通过 Mistral 欧盟托管的 API 
- **Coco Labs 发布首个设计模型 Vyb，可从品牌网站生成分层可编辑营销图** ｜· 不适用 ｜方向 其他
  - Coco Labs 发布其首个设计模型 Vyb，能根据品牌网站生成分层、可编辑的营销图形。Vyb 将每个元素放在独立图层，可只修改标题而无需重新生成整个设计；它能从公司网站识别 logo 和精确的十六进制色值，产品照片可以以全分辨率嵌入而不被重新生成，成品设计可导出至 Figma 并保留全部图层。
- **Coco Labs 推出 AI 设计模型 Vyb，分层输出可编辑设计稿** ｜· 不适用 ｜方向 其他
  - Coco Labs 的 AI 设计模型 Vyb 按图层逐个元素构建设计，文字保持可编辑文本、图形保持矢量、照片保持像素，并从网站自动提取 logo、字体和配色。在 145 款 Google 字体上按像素重叠 IoU 打分，Vyb 达到 90.3%，对比中 最强图像模型为 76.0%，该测试的测量上限为 94.4%。由于每层保留原生格式，导出 Figma 时结
- **MiniMax M3.1 Flash 登顶搜索效率榜** ｜✅ 已接入 ｜方向 其他 ｜网关模型 `qwenwork/flash`
  - 感谢 Parallel Web System 提供如此有意义的数据点~ 是的，MiniMax M3.1 Flash 现已在搜索能力排行榜的效率维度上位列第一。而且它很快~
- **Meta 发布 Muse Wonder Full (Max)，升至 Agent Arena 第 7 名、实验室第 4 位** ｜· 不适用 ｜方向 其他
  - Arena 宣布 Meta 的 Muse Wonder Full (Max) 在 Agent Arena 排名第 7，净提升 +11.3%，基于超 6.5K 真实智能体会话，将 Meta 推至实验室第 4 位。
- **SoMark 开源 1.3B 文档解析模型 OXR，登顶 olmOCR-Bench 等三榜** ｜· 不适用 ｜方向 代码
  - SoMark 团队发布开源文档解析模型 OXR（1.3B 参数），将 PDF 和文档图像转为含布局坐标的 Markdown 或 JSON 的 Agent-Friendly 数据。
- **ElevenLabs 发布两款面向实时 AI 对话的语音到语音模型 Eleven Realtime** ｜· 不适用 ｜方向 其他
  - ElevenLabs 于 10 月 20 日发布两款语音到语音模型 Eleven Realtime。
- **NVIDIA 发布 Cosmos3-H-Dreams 生成式手术模拟模型** ｜🆕 未接入 ｜方向 其他 ｜型号 Cosmos3-H-Dreams
  - NVIDIA 发布 Cosmos3-H-Dreams，将交互式生成模拟扩展到临床胆囊切除术场景，并称其为首个基于临床手术录像训练、支持实时运动学控制的生成式手术模拟器。
- **Perplexity Decider 在 Vals AI 金融基准上达帕累托最优** ｜· 不适用 ｜方向 其他
  - Perplexity Decider 在 Vals AI 的 Financial ClaimBench 上达到帕累托最优
- **Arena：OpenAI GPT-6 Luna 与 GPT-6.1 Sol 占据 Agent Arena Pareto 前沿 11 席中的 6 席** ｜· 不适用 ｜方向 其他
  - Arena 更新 Agent Arena Pareto 前沿，OpenAI 的 GPT-6 Luna 和 GPT-6.1 Sol 在不同推理档位下占据 11 个前沿位置中的 6 个，加上 GPT-6 Astra (Max) 共 7 席。
- **Jim Fan 开源机器人数据引擎模型套件 Flora，成本为 Astra 的 1/125** ｜· 不适用 ｜方向 代码
  - Jim Fan 宣布开源 Flora，一组用于解析物理世界、把原始视频转成训练信号的开放模型，称其以 125 倍更低的成本达到 Astra 级性能。Flora 已用于其内部数据引擎，在 500 块 GPU 上每天标注 20 万小时视频，提供带时间戳的高质量字幕、用于质量控制和 RL 后训练的密集进度奖励，以及用于现实基准测试的 rubrics 评分。
- **fal 发布 FLUX 3 Max，图生视频 Elo 达 1139 并列第一** ｜· 不适用 ｜方向 其他
  - fal 发布与 Black Forest Labs 合作后训练的视频模型 FLUX 3 Max，在第三方独立人类偏好评测中获 1139 Elo，与 Seedance 2.5 并列图生视频质量第一梯队。该模型约 12 秒生成一段 10 秒 720/768p 视频，未来三周降价 75%，后续还将继续后训练改进。
- **OpenAI 称 GPT-6 在 COBOL、Fortran 等遗留编程语言上大幅提升** ｜· 不适用 ｜方向 代码
  - OpenAI 表示最新模型针对 COBOL、Fortran、Visual Basic 等低资源语言做了改进，这些语言训练代码少但支撑大量关键基础设施，IBM 估计 COBOL 支撑超过 40% 的网上银行系统和 95% 的 ATM 交易。
- **Mistral 发布 Voxtral 3 语音模型套件** ｜🆕 未接入 ｜方向 代码 ｜型号 Voxtral 3
  - 我们刚刚发布了一套全面的 SOTA 语音模型 https://mistral.ai/news/voxtral-3/ 。语音将成为与 AI 系统交互最重要的接口，我们将语音模型部署在物理上靠近推理模型的位置
- **Artificial Analysis：Intelligence Index 各档位智能成本一年内大幅下降** ｜· 不适用 ｜方向 金融
  - Artificial Analysis 分析 Intelligence Index 各阈值达成的成本变化：达到 30 分如今每任务 0.03 美元（GPT-6 Luna high）。
- **Artificial Analysis 评测 Mistral Voxtral 3 语音模型：Small Transcribe 3 位列语音转文本榜单第 3** ｜🆕 未接入 ｜方向 其他 ｜型号 Voxtral 3
  - Artificial Analysis 评测了 Mistral 发布的 Voxtral 3 语音模型，包括 1 个 TTS 模型和 3 个语音转文本模型。
- **Artificial Analysis 评测 Bria Fibo 2.0：开源权重图像模型登顶 AA 图像编辑榜单** ｜🆕 未接入 ｜方向 代码 ｜型号 Fibo 2.0
  - Artificial Analysis 评测 Bria 的 8B 开源权重图像模型 Fibo 2.0，称其以 AA-Image-Editing v2.1 榜首、并在 AA-Image-T2I v2.1 上与 Qwen-Image-2.1 统计上并列领先，较第一代 Fibo 在所有编辑动作和文生图能力上均有提升。
- **Artificial Analysis 评测 Krea 3 Ultra：AA-Image-Editing v2.1 排名第 5** ｜· 不适用 ｜方向 其他
  - Artificial Analysis 将 Krea 3 Ultra 测入 AA-Image-Editing v2.1 榜单，排名第 5，质量接近 Nano Banana 2.1 与 MAI-Image-2.6，是 OpenAI、Google、Microsoft 之外排名最高的图像编辑模型。
- **Artificial Analysis 评测 Mistral Voxtral 3 语音模型：Small Transcribe 3 列语音转文字榜第三** ｜🆕 未接入 ｜方向 其他 ｜型号 Voxtral 3
  - Artificial Analysis 评测了 Mistral 新发布的 Voxtral 3 系列语音模型，包括 1 个 TTS 和 3 个语音转文字模型。
- **Mistral 发布 Voxtral 3 Transcribe 和 Speech 模型并推出语音智能体 API** ｜🆕 未接入 ｜方向 代码 ｜型号 Voxtral 3
  - Mistral AI 发布 Voxtral 3 系列，包含 Transcribe 和 Speech 两个语音模型，称其达到业界领先水平。两个模型为 Mistral 新推出的语音智能体 API 提供支持。
- **Krea 3 Ultra 进入 Arena 单图与多图编辑竞技场，多图编辑列第 4** ｜· 不适用 ｜方向 其他
  - Arena 宣布 Krea 3 Ultra 登上 Single-Image Edit Arena 和 Multi-Image Edit Arena，Krea 跻身两个榜单按实验室计前 5。
- **Krea 3 Ultra 与 Fast 登图像编辑榜前五** ｜· 不适用 ｜方向 其他
  - Krea 3 Ultra 在 Artificial Analysis 图像编辑榜以 1151 分位列第 4，仅落后 Google 的 Nano Banana 2.1 一分；Krea 3 Fast 以 1125 分排第 11，反超 Nano Banana 2 一分。
- **Krea 3 登顶图像竞技场** ｜· 不适用 ｜方向 金融
  - 今天，Krea 3 登上了图像竞技场的榜首。 - “Fast”推动了速度与质量帕累托曲线的边界。 - “Ultra”排名前四，仅被 OpenAI 模型超越。 是前十名中唯一估值低于 1 万亿美元的公司！ 更多内容见下方 👇
- **Artificial Analysis 盘点上周美国开源权重模型进展：Nemotron 3.5、Muse Spark Open、Beam 1.0** ｜🆕 未接入 ｜方向 代码 ｜型号 Nemotron 3.5
  - Artificial Analysis 盘点上周美国开源权重模型在智能和参数效率上的进展。
- **ElevenLabs 发布 Eleven Realtime 语音到语音模型** ｜· 不适用 ｜方向 其他
  - ElevenLabs 发布 Eleven Realtime，一类新的语音到语音（Speech to Speech）模型。官方称语音智能体通常需要在快速回复和准确回答之间取舍，Eleven Realtime 两者兼顾，能在半秒内开始说话，并答对口语推理问题。
- **Rohan Paul 谈 Qwen3.8-27B RL post-train 的智能体表现：幻觉率从 30.4% 降至 15.1%** ｜🆕 未接入 ｜方向 代码 ｜型号 Qwen3.8-27B
  - Rohan Paul 观察到今年不少亮眼 Agent 结果来自小开源模型的 post-train。
- **面壁 MiniCPM-V 4.7 在 iPhone 18 Pro Max 上实现 20.51 tokens/sec 本地多模态推理** ｜🆕 未接入 ｜方向 代码 ｜型号 MiniCPM-V 4.7
  - OpenBMB 宣布 MiniCPM-V 4.7 在 iPhone 18 Pro Max（12GB）上实现平均 20.51 tokens/sec 的本地解码速度，较未优化的 SSD 专家加载基线提速 6.07×。提速来自 Lookahead Expert Scheduling（LES）、优化专家加载、细粒度量化与 DSpark 投机解码，GitHub 和 H
- **OpenAI 或准备发布 GPT-6.1 Terra** ｜· 不适用 ｜方向 其他
  - OpenAI 似乎也在准备发布 GPT-6.1 Terra 模型。 > 该模型引用最近出现在微软的 PR 评测配置中。 > 此前，《The Information》报道称该模型也在开发中。

## 二、今日热议（热度面，交叉参考）

- DeepSeek 开源内部推理框架 DeepInfer
- MiniMax 发布 M3.1 Flash，10 月 23 日开放权重
- 美土安全部令联邦文职机构移除DeepSeek及关联产品
- DeepSeek 发布 V4.1-Flash-1017 并开放搜索 API
- OpenAI收购药物研发平台Orchestra Bio
- Google 将 Gemini 个人智能引入车载系统
- Google 与 Meta 开源 TorchTPU，Hugging Face 原生支持 TPU
- SpaceX 三季度 AI 业务收入占比过半并扭亏为盈
- ChatGPT上线锁定聊天，全套餐可PIN或生物识别保护
- OpenAI 拟以超1.4万亿美元估值融资300亿美元

