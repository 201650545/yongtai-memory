---
name: reference_aihot_模型动态日报
description: AIHOT 模型类动态日报（新品发布面），每日定时任务覆盖刷新；每条标注方向与是否已接入本机网关。
type: reference
updated: 2026-10-29
---
# AIHOT 模型动态日报（每日）

> **同步时间**：2026-10-29 01:10:02（每日定时任务自动刷新落盘）
> **数据来源**：https://aihot.news/api/v1/items?mode=all&category=ai-models&window=24h
> **口径**：这是**新品/新发布面**（不是能力榜，也不是热度榜）——「AI 圈最近发布了什么模型」。
> **接入判定**：`✅ 已接入` = 该型号已在本机网关（:8787）模型清单里；`🆕 未接入` = 有型号但网关里没有，
> 值得评估接入；`· 不适用` = 这条是框架/工具/生态类，不是可接入的对话模型。

## 一、模型动态（过去 24h）

- **Artificial Analysis 发布 AA-Video-I2V v2.1 图像生视频评测基准** ｜🆕 未发现目录匹配 ｜方向 其他 ｜型号 AA-Video-I2V
  - Artificial Analysis 发布 AA-Video-I2V v2.1 与 AA-Video-I2V-Silent v2.1 图像生视频评测基准，在 1080p 下按 10 类用例、10 项能力和多种视觉风格对模型排名。
- **AssemblyAI 发布首个语音合成模型 AssemblyAI-TTS-1，进入 Provider Voice Arena 前 12** ｜🆕 未发现目录匹配 ｜方向 其他 ｜型号 AssemblyAI-TTS-1
  - Artificial Analysis 评测了 AssemblyAI 发布的首个语音合成模型 AssemblyAI-TTS-1。该模型在 Provider Voice Arena 以 Elo 1,227 排名第 12，在 Controlled Voice 排名第 10，发音鲁棒性得分 81.7% 排名第 16。
- **Artificial Analysis 评测 GitHub 新发布的 Copilot Fusion：得分略低于 Opus 5.5，成本减半** ｜✅ 目录型号级命中（API 可调用性未核验） ｜方向 代码 ｜网关模型 `cline/anthropic/claude-opus-5.5`
  - Artificial Analysis 在 Coding Agent Index v2.0 中评测 GitHub 新发布的 Copilot Fusion，该系统在 Anthropic 与 OpenAI 模型间动态编排，得分比 Claude Code 中的 Opus 5.5 低 2 分。
- **Nvidia 开源 Nemotron 3.5 Transcribe 语音识别模型，集成转写、翻译和说话人识别** ｜🔶 目录家族级命中，变体待核 ｜方向 代码 ｜网关模型 `cline/cline-free/nemotron-3.5-super-vl`
  - Nvidia 发布开源语音识别模型 Nemotron 3.5 Transcribe，可转写 40 种语言、在 31 种语言与英语间互译、识别最多 8 个说话人，支持最长 1 小时的录音，并能通过提示词控制输出或回答音频内容问题。
- **面壁智能发布 MiniCPM-OCR 1.0，支持在 iPhone 和 iPad 本地运行** ｜🆕 未发现目录匹配 ｜方向 其他 ｜型号 MiniCPM-OCR 1.0
  - 面壁智能 OpenBMB 发布 MiniCPM-OCR 1.0，主打 1B 规模下的 SOTA OCR 性能与速度，在 Real5-OmniDocBench 得 93.68、OCRBench v2 得 54.7，并演示在 iPhone 和 iPad 上本地运行。
- **Nvidia 发布开源语音转写模型 Nemotron 3.5 Transcribe，支持 40 种语言** ｜🔶 目录家族级命中，变体待核 ｜方向 代码 ｜网关模型 `cline/cline-free/nemotron-3.5-super-vl`
  - Nvidia 发布免费开放权重的语音转写模型 Nemotron 3.5 Transcribe，支持最多 40 种语言，可处理最长 1 小时的录音并区分最多 8 个说话人，还同步发布了第 2 版开源语音数据集 Granary。
- **NVIDIA 发布 Nemotron 3.5 Transcribe，2.8% WER 并列开放权重语音转文本第一** ｜🔶 目录家族级命中，变体待核 ｜方向 其他 ｜网关模型 `cline/cline-free/nemotron-3.5-super-vl`
  - NVIDIA 发布开放权重语音转文本模型 Nemotron 3.5 Transcribe，在 Artificial Analysis 非流式榜单上以 2.8% WER 与 Mistral Voxtral Small 并列开放权重第一，总参数 30B、激活 4B。
- **NVIDIA 发布开放权重语音模型 Nemotron 3.5 Transcribe 及 Granary v2 数据管线** ｜🔶 目录家族级命中，变体待核 ｜方向 其他 ｜网关模型 `cline/cline-free/nemotron-3.5-super-vl`
  - NVIDIA 发布开放权重语音模型 Nemotron 3.5 Transcribe，现已在 Hugging Face 和 ModelScope 提供，单一模型支持 40 种语言转写、31 种语言翻译、13 种语言说话人分离和音频问答，可处理最长一小时、最多 8 个说话人的录音。
- **Artificial Analysis 新版 Intelligence Index 扩大开源与闭源模型差距** ｜· 不适用（非具体模型） ｜方向 代码
  - Artificial Analysis 改版其 Intelligence Index 至版本 5，Kimi K3.1 Pro 从第 4 降至第 9，开源模型与榜首差距从 3 分扩大到 12 分，Grok 4.7 也下跌 12 分。
- **AtomicChat 实测 MiniCPM-OCR 1.0 在 MacBook 上本地解析 Anthropic 全部 415 页 S-1 文件** ｜🆕 未发现目录匹配 ｜方向 其他 ｜型号 MiniCPM-OCR 1.0
  - OpenBMB 转发并感谢 @atomic_chat_hq 的演示：该演示在 M5 Max MacBook 上本地运行 MiniCPM-OCR 1.0，处理 Anthropic S-1 文件全部 415 页，1.2GB 模型约每页 4 秒，数据全程不离开设备。GGUF 权重已发布在 huggingface.co/AtomicChat/MiniCPM-OCR-
- **面壁智能开源 MiniCPM-OCR 系列，文档解析与 OCR 结果可靠性评估配套** ｜· 不适用（非具体模型） ｜方向 代码
  - OpenBMB 开源 MiniCPM-OCR 系列模型，把文档解析与 OCR 结果可靠性评估配套提供。MiniCPM-OCR 1.0 是 1.3B 参数的中英文文档解析模型，支持扫描页、拍照文档、倾斜和弯曲页面，可处理表格、公式、PDF 和关键信息抽取，并支持查看 Markdown 源码与预览解析结果；MiniCPM-OCR Jev 是独立模型，用于评估 O
- **商汤开源 SenseNova 6.8 Code2Video：用代码生成短视频** ｜🔶 目录家族级命中，变体待核 ｜方向 代码 ｜网关模型 `raccoon/sn-sensenova-6-8-flash`
  - 商汤发布并开源 SenseNova 6.8 Code2Video 轻量级模型，通过生成可执行代码来创作和渲染短视频。模型权重和 Skill 已在 Hugging Face 和 GitHub 开放下载，并附上每条演示视频的提示词与完整生成轨迹；官方称未来将探索视频编辑、动画和 3D 创建。
- **面壁智能发布并开源 MiniCPM-OCR 系列：1.3B 解析模型与 2B 判别模型** ｜· 不适用（非具体模型） ｜方向 代码
  - 面壁智能发布并开源 MiniCPM-OCR 系列。MiniCPM-OCR 1.0（1.3B）在 Real5-OmniDocBench 取得 93.68 分、OCRBench v2 取得 54.7 分的 SOTA，经 DSpark 加速后吞吐达 1.217 页/秒，端到端效率提升 55%。
- **Liquid AI 发布 LFM3 模型家族，首批多款模型均基于 LFM3-1.7B-Base** ｜🆕 未发现目录匹配 ｜方向 其他 ｜型号 LFM3-1.7B-Base
  - Liquid AI 于当地时间 27 日发布 LFM3 模型家族，采用全新的三混合层架构，在 22T 词元上预训练。首批包括 LFM-1.7B（文本）、LFM3-VL-2B（视觉）、d1-2B（决策）、LFM3-Audio（音频）、LFM3-Omni-2B（全能）和 d1-Omni-2B（全能决策），均基于 LFM3-1.7B-Base。
- **Google DeepMind 发布 Genie 4 实时世界模型，原生生成音频并由 Gemini 3.8 Flash 在循环中规划** ｜🆕 未发现目录匹配 ｜方向 其他 ｜型号 Genie 4
  - Google DeepMind 发布 Genie 4 世界模型研究预览，可从文本和图像提示实时生成可探索世界，并原生生成环境音、音乐和角色对话。架构上由 Gemini Omni 锚定世界外观，Gemini 3.8 Flash 在模拟循环内解释提示、拆解目标、校验帧并重规划。
- **面壁智能 OpenBMB 回应第三方对 MiniCPM-OCR 的评测** ｜· 不适用（非具体模型） ｜方向 代码
  - 面壁智能 OpenBMB 转评 @wikiwayne 对 MiniCPM-OCR 的评测，感谢其透明对比并分享了结果与注意事项，表示期待该模型在 GX10 上的本地测试表现，称这类真实反馈会推动模型持续改进。引用内容提到 MiniCPM-OCR 1.0 为开源 13 亿参数 OCR 模型，与评估结果可靠性的 MiniCPM-OCR Jev 配套，权重已开放于
- **微软发布 MAI-Image-2.7-Preview 图像编辑模型，AA-Image-Editing v2.1 榜单排名第二** ｜🆕 未发现目录匹配 ｜方向 其他 ｜型号 MAI-Image-2.7-Preview
  - 微软于 10 月 27 日推出图像编辑模型 MAI-Image-2.7-Preview，在 Artificial Analysis 的 AA-Image-Editing v2.1 榜单以 1,193 Elo 排名第二，仅次于 OpenAI 的 GPT Image 2.5 Sunburst (max)。
- **Artificial Analysis 发布 Intelligence Index v5 评测基准** ｜· 不适用（非具体模型） ｜方向 其他
  - Artificial Analysis 发布 Intelligence Index v5，引入 FrontierCode 2.0 和 Terminal-Bench-Science 两个新基准，并升级 HLE-Diamond、AA-Omniscience v1.1 和 CritPt v2，60% 的指数基于私有测试集或保留答案。
- **谷歌更新 Android Bench 榜单：Gemini 4 Argon 编程能力落后于 Claude 与 GPT** ｜🔶 目录家族级命中，变体待核 ｜方向 代码 ｜网关模型 `cline/google/gemini-4-argon`
  - 谷歌更新评估安卓编程辅助能力的 Android Bench 榜单，新增 GPT-6 Sol、GPT-6.1 Sol、Claude Sonnet 5、Claude Sonnet 5.5 和 Gemini 4 Argon 的成绩，并标注各模型推理等级。
- **Artificial Analysis 发布 Intelligence Index v5 并首次推出 Progress Index v1** ｜· 不适用（非具体模型） ｜方向 其他
  - Artificial Analysis 发布 Intelligence Index v5，新增 FrontierCode 2.0 和 Terminal-Bench-Science 两项基准，升级 HLE-Diamond、AA-Omniscience v1.1 和 CritPt v2，60% 的指数基于私有测试集。
- **Google 发布世界模型 Genie 4，支持实时操控与原生音频** ｜🆕 未发现目录匹配 ｜方向 其他 ｜型号 Genie 4
  - Google 正式发布下一代世界模型 Genie 4，距上一代 Genie 3 发布过去14个月。相比 Genie 3，它具备更强的照片级真实感、物体碰撞等物理模拟能力，支持键盘或双摇杆实时控制，并可用自然语言修改天气、加入物体和改变事件。
- **蚂蚁百灵发布灵光 2.0 并开源 Ling-3.1-flash-base 与 Ling-3.1-flash-1019** ｜🔶 目录家族级命中，变体待核 ｜方向 代码 ｜网关模型 `antling/Ling-3.1-flash`
  - 蚂蚁百灵 10 月 27 日发布灵光 2.0，升级为能主动跟进任务、持续管理复杂事务的个人 AI 助理，并开源了 Ling-3.1-flash-base 与 Ling-3.1-flash-1019。
- **Google 发布世界模型 Genie 4，支持实时操控与原生音频** ｜🆕 未发现目录匹配 ｜方向 其他 ｜型号 Genie 4
  - Google 发布下一代世界模型 Genie 4，相比 Genie 3 在照片级真实感、物体碰撞等物理模拟上有明显进步。用户可用 WASD 和双摇杆实时控制角色或镜头，运行中可用自然语言修改天气和加入物体，模型还能同步生成环境音与人物实时对话。
- **谷歌 DeepMind 发布 Genie 4 世界模型，皮查伊称其为迄今最逼真、最具互动性** ｜🆕 未发现目录匹配 ｜方向 其他 ｜型号 Genie 4
  - 谷歌 DeepMind 于 10 月 27 日发布 Genie 4 世界模型，定位为重大研究里程碑，用户可用自然语言实时改变模拟世界，如改天气、移动镜头、加入新角色，并原生生成与画面同步的音频，物理表现和人物动作也更真实。
- **Google DeepMind 发布交互式世界模型 Genie 4** ｜🆕 未发现目录匹配 ｜方向 其他 ｜型号 Genie 4
  - Demis Hassabis 宣布 Genie 4 发布，称其结合实时物理、推理与音频，并暗示“模拟中的模拟”。引用的 @GoogleDeepMind 介绍称 Genie 4 是迄今最逼真、交互性最强的世界模型，可实时探索动态环境，观察场景响应、声音以及其中人物的移动、反应和说话。
- **谷歌 DeepMind 发布世界模型 Genie 4：一句话生成可交互虚拟世界并同步音频** ｜🆕 未发现目录匹配 ｜方向 其他 ｜型号 Genie 4
  - 谷歌 DeepMind 于周二推出世界模型 Genie 4，处于研究预览阶段，可生成拟真度更高的可交互虚拟世界，并首次实现与画面同步的实时音频，包括音乐、环境音和可交互对话。
- **Cartesia Managed Agents 语音智能体 Elo 达 1115** ｜· 不适用（非具体模型） ｜方向 其他
  - Cartesia Managed Agents 在 Artificial Analysis Speech Agent Arena 上取得 1115 的 Elo，比此前的语音智能体产品 Cartesia Line（1017）高 98 分，任务成功率从 77.5% 提升至 91.7%。
- **Liquid AI 发布 LFM3：6 个开源权重 2B 级多模态模型** ｜· 不适用（非具体模型） ｜方向 代码
  - Liquid AI 发布 LFM3 系列共 6 个开源权重 2B 级模型，基于同一 tri-hybrid 骨干覆盖文本、视觉、音频、omni 和决策任务。
- **蚂蚁 Ling 3.1 Flash 1019 开源模型评测提升至 44 分** ｜🔶 目录家族级命中，变体待核 ｜方向 代码 ｜网关模型 `antling/Ling-3.1-flash`
  - 蚂蚁 Ling 3.1 Flash 1019 以 MIT 协议开源，560B 总参数、25B 激活参数、1M token 上下文，在 Artificial Analysis Intelligence Index v4.3 上得分 44，较前代 Ling 3.1 Flash 的 41 分提升 3 分。
- **Liquid AI 发布 LFM3 系列：一个 1.7B 底座衍生六个 2B 级多模态模型** ｜· 不适用（非具体模型） ｜方向 其他
  - Liquid AI 在 Hugging Face 发布 LFM3 系列，以 LFM3-1.7B-Base 为共享底座，提供文本、视觉、音频、全模态和决策共六个 2B 级模型，均开放权重。

## 二、今日热议（热度面，交叉参考）

- Google DeepMind 发布 Genie 4 世界模型研究预览版
- Anthropic 递交 S-1，拟以 ANT 登陆纳斯达克
- OpenAI 发布 GPT-6.1 Terra，API 价格减半
- OpenAI 称三项科学发现，物理证明未公开引呼吁
- Anthropic公布药物研发合作，并传收购Mithril Medicine
- Anthropic 一团队取消编程面试，改看原型
- Artificial Analysis 发布 v5 指数，开源模型差距扩大
- OpenAI 拟采购谷歌 TPU 并招募工程师适配
- 蚂蚁发布灵光2.0，AI助理可跨会话持续办事
- 英伟达与Meta扩大Muse合作并投资30亿美元

